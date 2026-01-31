"""Installation page"""
import json
import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QProgressBar,
)
from PyQt6.QtCore import QThread, pyqtSignal


class InstallationWorker(QThread):
    """Worker thread for installation tasks"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        """Run installation"""
        try:
            # Get repository path
            # __file__ is installer/src/installer/pages/install.py
            # Go up 5 levels: pages/ -> installer/ -> src/ -> installer/ -> repo root
            repo_path = Path(__file__).parent.parent.parent.parent.parent.absolute()
            self.progress.emit(f"📁 Repository path: {repo_path}")
            self.progress.emit(f"📁 Path exists: {repo_path.exists()}")

            # List subdirectories to verify
            if repo_path.exists():
                subdirs = [d.name for d in repo_path.iterdir() if d.is_dir()]
                self.progress.emit(f"📁 Found directories: {', '.join(subdirs)}")

            # Create MCP configuration
            self.progress.emit("\n📝 Creating MCP configuration...")
            mcp_config = self._create_mcp_config(repo_path)

            # Write to Claude Code settings
            settings_path = Path.home() / ".claude" / "settings.json"
            self.progress.emit(f"💾 Writing to: {settings_path}")

            self._update_claude_settings(settings_path, mcp_config)
            self.progress.emit("✅ MCP configuration updated")

            # Install dependencies for each enabled MCP server
            if self.config.get("wifi_camera_enabled"):
                self.progress.emit("\n📦 Installing wifi-cam-mcp dependencies...")
                wifi_cam_path = repo_path / "wifi-cam-mcp"
                if not wifi_cam_path.exists():
                    raise Exception(f"wifi-cam-mcp directory not found at {wifi_cam_path}")
                self._run_uv_sync(wifi_cam_path)

            if self.config.get("usb_camera_enabled"):
                self.progress.emit("\n📦 Installing usb-webcam-mcp dependencies...")
                usb_cam_path = repo_path / "usb-webcam-mcp"
                if not usb_cam_path.exists():
                    raise Exception(f"usb-webcam-mcp directory not found at {usb_cam_path}")
                self._run_uv_sync(usb_cam_path)

            if self.config.get("memory_enabled"):
                self.progress.emit("\n📦 Installing memory-mcp dependencies...")
                memory_path = repo_path / "memory-mcp"
                if not memory_path.exists():
                    raise Exception(f"memory-mcp directory not found at {memory_path}")
                self._run_uv_sync(memory_path)

            self.progress.emit("\n✅ Installation completed successfully!")
            self.finished.emit(True, "Installation completed")

        except Exception as e:
            error_msg = f"Installation failed: {str(e)}"
            self.progress.emit(f"\n❌ {error_msg}")
            self.finished.emit(False, error_msg)

    def _create_mcp_config(self, repo_path):
        """Create MCP server configuration"""
        config = {"mcpServers": {}}

        # Wi-Fi camera
        if self.config.get("wifi_camera_enabled"):
            config["mcpServers"]["wifi-cam"] = {
                "command": "uv",
                "args": [
                    "--directory",
                    str(repo_path / "wifi-cam-mcp"),
                    "run",
                    "wifi-cam-mcp",
                ],
                "env": {
                    "TAPO_CAMERA_HOST": self.config.get("tapo_host", ""),
                    "TAPO_USERNAME": self.config.get("tapo_username", ""),
                    "TAPO_PASSWORD": self.config.get("tapo_password", ""),
                },
            }

        # USB camera
        if self.config.get("usb_camera_enabled"):
            config["mcpServers"]["usb-webcam"] = {
                "command": "uv",
                "args": [
                    "--directory",
                    str(repo_path / "usb-webcam-mcp"),
                    "run",
                    "usb-webcam-mcp",
                ],
            }

        # Memory
        if self.config.get("memory_enabled"):
            config["mcpServers"]["memory"] = {
                "command": "uv",
                "args": [
                    "--directory",
                    str(repo_path / "memory-mcp"),
                    "run",
                    "memory-mcp",
                ],
            }

        # System temperature
        config["mcpServers"]["system-temperature"] = {
            "command": "uv",
            "args": [
                "--directory",
                str(repo_path / "system-temperature-mcp"),
                "run",
                "system-temperature-mcp",
            ],
        }

        return config

    def _update_claude_settings(self, settings_path, mcp_config):
        """Update Claude Code settings.json"""
        settings_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing settings
        existing = {}
        if settings_path.exists():
            with open(settings_path, "r") as f:
                existing = json.load(f)

        # Merge MCP servers
        if "mcpServers" not in existing:
            existing["mcpServers"] = {}

        existing["mcpServers"].update(mcp_config["mcpServers"])

        # Write back
        with open(settings_path, "w") as f:
            json.dump(existing, f, indent=2)

    def _run_uv_sync(self, directory):
        """Run uv sync in a directory"""
        self.progress.emit(f"Running uv sync in: {directory}")

        # Ensure directory exists
        if not directory.exists():
            raise Exception(f"Directory does not exist: {directory}")

        try:
            result = subprocess.run(
                ["uv", "sync"],
                cwd=str(directory),  # Convert Path to string for Windows compatibility
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )

            if result.returncode != 0:
                raise Exception(f"uv sync failed in {directory.name}: {result.stderr}")

            self.progress.emit(result.stdout)
        except subprocess.TimeoutExpired:
            raise Exception(f"uv sync timed out in {directory.name}")


class InstallationPage(QWizardPage):
    """Run installation"""

    def __init__(self):
        super().__init__()
        self.setTitle("Installation")
        self.setSubTitle("Installing Embodied Claude MCP servers")

        layout = QVBoxLayout()

        # Progress label
        self.progress_label = QLabel("Ready to install...")
        layout.addWidget(self.progress_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

        # Installation worker
        self.worker = None
        self.installation_complete = False

    def initializePage(self):
        """Start installation when page is shown"""
        # Gather configuration from previous pages
        config = {
            "wifi_camera_enabled": self.field("wifi_camera_enabled"),
            "tapo_host": self.field("tapo_host"),
            "tapo_username": self.field("tapo_username"),
            "tapo_password": self.field("tapo_password"),
            "usb_camera_enabled": self.field("usb_camera_enabled"),
            "memory_enabled": self.field("memory_enabled"),
            "api_key": self.field("api_key"),
        }

        # Start installation
        self.progress_label.setText("Installing...")
        self.progress_bar.show()
        self.log_output.clear()

        self.worker = InstallationWorker(config)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_progress(self, message):
        """Handle progress updates"""
        self.log_output.append(message)

    def _on_finished(self, success, message):
        """Handle installation completion"""
        self.progress_bar.hide()
        self.installation_complete = success

        if success:
            self.progress_label.setText("✅ Installation completed!")
            self.progress_label.setStyleSheet("QLabel { color: green; font-weight: bold; }")
        else:
            self.progress_label.setText(f"❌ Installation failed: {message}")
            self.progress_label.setStyleSheet("QLabel { color: red; font-weight: bold; }")

        self.completeChanged.emit()

    def isComplete(self):
        """Page is complete when installation finishes successfully"""
        return self.installation_complete
