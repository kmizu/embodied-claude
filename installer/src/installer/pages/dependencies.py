"""Dependencies check page"""
import shutil
import subprocess
import sys
from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextBrowser,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon


class DependenciesPage(QWizardPage):
    """Check and install required dependencies"""

    def __init__(self):
        super().__init__()
        self.setTitle("Dependencies Check")
        self.setSubTitle(
            "Checking required software (ffmpeg, OpenCV, Whisper)"
        )

        layout = QVBoxLayout()

        # Status label
        self.status_label = QLabel("Checking dependencies...")
        layout.addWidget(self.status_label)

        # Dependencies list
        self.deps_list = QListWidget()
        layout.addWidget(self.deps_list)

        # Installation instructions
        self.instructions = QTextBrowser()
        self.instructions.setOpenExternalLinks(True)
        self.instructions.setMaximumHeight(200)
        self.instructions.hide()
        layout.addWidget(self.instructions)

        # Recheck button
        self.recheck_button = QPushButton("Recheck Dependencies")
        self.recheck_button.clicked.connect(self.check_dependencies)
        self.recheck_button.hide()
        layout.addWidget(self.recheck_button)

        layout.addStretch()
        self.setLayout(layout)

        # Track completion status
        self.all_satisfied = False

    def initializePage(self):
        """Called when page is shown"""
        # Delay check to let UI render first
        QTimer.singleShot(100, self.check_dependencies)

    def check_dependencies(self):
        """Check all required dependencies"""
        self.deps_list.clear()
        self.status_label.setText("Checking dependencies...")

        results = {
            "ffmpeg": self._check_ffmpeg(),
            "Python": self._check_python(),
            "OpenCV": self._check_opencv(),
            "uv": self._check_uv(),
        }

        # Display results
        for name, (installed, version) in results.items():
            item = QListWidgetItem()
            if installed:
                item.setText(f"✅ {name}: {version}")
                item.setForeground(Qt.GlobalColor.darkGreen)
            else:
                item.setText(f"❌ {name}: Not found")
                item.setForeground(Qt.GlobalColor.red)
            self.deps_list.addItem(item)

        # Check if all satisfied
        self.all_satisfied = all(installed for installed, _ in results.values())

        if self.all_satisfied:
            self.status_label.setText("✅ All dependencies satisfied!")
            self.status_label.setStyleSheet("QLabel { color: green; font-weight: bold; }")
            self.instructions.hide()
            self.recheck_button.hide()
        else:
            self.status_label.setText("⚠️ Some dependencies are missing")
            self.status_label.setStyleSheet("QLabel { color: orange; font-weight: bold; }")
            self._show_install_instructions(results)
            self.instructions.show()
            self.recheck_button.show()

        # Update wizard buttons
        self.completeChanged.emit()

    def isComplete(self):
        """Page is complete only if all dependencies are satisfied"""
        return self.all_satisfied

    def _check_ffmpeg(self):
        """Check if ffmpeg is installed"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                version = result.stdout.split("\n")[0].split(" ")[2]
                return True, version
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return False, None

    def _check_python(self):
        """Check Python version"""
        version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        return True, version

    def _check_opencv(self):
        """Check if OpenCV is installed"""
        try:
            import cv2
            return True, cv2.__version__
        except ImportError:
            return False, None

    def _check_uv(self):
        """Check if uv is installed"""
        if shutil.which("uv"):
            try:
                result = subprocess.run(
                    ["uv", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    version = result.stdout.strip().split(" ")[1]
                    return True, version
            except (subprocess.TimeoutExpired, IndexError):
                pass
        return False, None

    def _show_install_instructions(self, results):
        """Show installation instructions for missing dependencies"""
        html_parts = ["<h3>Installation Instructions</h3>"]

        if not results["ffmpeg"][0]:
            html_parts.append(
                """
                <h4>ffmpeg</h4>
                <ul>
                    <li><strong>Windows:</strong> <code>winget install ffmpeg</code></li>
                    <li><strong>Mac:</strong> <code>brew install ffmpeg</code></li>
                    <li><strong>Linux:</strong> <code>sudo apt install ffmpeg</code></li>
                </ul>
                """
            )

        if not results["OpenCV"][0]:
            html_parts.append(
                """
                <h4>OpenCV</h4>
                <p>Will be installed automatically with uv during MCP server setup.</p>
                """
            )

        if not results["uv"][0]:
            html_parts.append(
                """
                <h4>uv (Python Package Manager)</h4>
                <p>Install from: <a href="https://github.com/astral-sh/uv">
                https://github.com/astral-sh/uv</a></p>
                <ul>
                    <li><strong>Windows/Mac/Linux:</strong>
                    <code>curl -LsSf https://astral.sh/uv/install.sh | sh</code></li>
                </ul>
                """
            )

        self.instructions.setHtml("".join(html_parts))
