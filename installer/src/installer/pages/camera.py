"""Camera selection page"""
from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QGroupBox,
    QLineEdit,
    QFormLayout,
    QCheckBox,
    QWidget,
)
from PyQt6.QtCore import Qt


class CameraSelectionPage(QWizardPage):
    """Select cameras to use"""

    def __init__(self):
        super().__init__()
        self.setTitle("Camera Selection")
        self.setSubTitle("Select cameras for Embodied Claude")

        layout = QVBoxLayout()

        # Wi-Fi Camera (Tapo) section
        wifi_group = QGroupBox("Wi-Fi PTZ Camera (Recommended)")
        wifi_layout = QVBoxLayout()

        self.use_wifi_camera = QCheckBox("Use Wi-Fi Camera (TP-Link Tapo)")
        self.use_wifi_camera.setChecked(True)
        self.use_wifi_camera.stateChanged.connect(self._on_wifi_camera_changed)
        wifi_layout.addWidget(self.use_wifi_camera)

        # WiFi camera configuration form
        self.wifi_form = QWidget()
        wifi_form_layout = QFormLayout()

        self.tapo_host = QLineEdit()
        self.tapo_host.setPlaceholderText("192.168.1.xxx")
        wifi_form_layout.addRow("Camera IP:", self.tapo_host)

        self.tapo_username = QLineEdit()
        self.tapo_username.setPlaceholderText("admin")
        wifi_form_layout.addRow("Username:", self.tapo_username)

        self.tapo_password = QLineEdit()
        self.tapo_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.tapo_password.setPlaceholderText("Password")
        wifi_form_layout.addRow("Password:", self.tapo_password)

        self.wifi_form.setLayout(wifi_form_layout)
        wifi_layout.addWidget(self.wifi_form)

        # Note about Tapo setup
        tapo_note = QLabel(
            "📝 Note: Create a local account on your Tapo camera first\n"
            "(Camera Settings → Advanced → Camera Account)"
        )
        tapo_note.setWordWrap(True)
        tapo_note.setStyleSheet("QLabel { color: #666; margin-top: 5px; }")
        wifi_layout.addWidget(tapo_note)

        wifi_group.setLayout(wifi_layout)
        layout.addWidget(wifi_group)

        # USB Camera section
        usb_group = QGroupBox("USB Webcam (Optional)")
        usb_layout = QVBoxLayout()

        self.use_usb_camera = QCheckBox("Use USB Webcam")
        self.use_usb_camera.stateChanged.connect(self._on_usb_camera_changed)
        usb_layout.addWidget(self.use_usb_camera)

        self.usb_camera_list = QListWidget()
        self.usb_camera_list.setEnabled(False)
        usb_layout.addWidget(self.usb_camera_list)

        scan_button = QPushButton("Scan USB Cameras")
        scan_button.clicked.connect(self._scan_usb_cameras)
        usb_layout.addWidget(scan_button)

        usb_group.setLayout(usb_layout)
        layout.addWidget(usb_group)

        # Memory MCP section
        memory_group = QGroupBox("Long-term Memory (Brain)")
        memory_layout = QVBoxLayout()

        self.use_memory = QCheckBox("Enable long-term memory (ChromaDB)")
        self.use_memory.setChecked(True)
        memory_layout.addWidget(self.use_memory)

        memory_note = QLabel(
            "💡 Memories will be stored in ~/.claude/memories/"
        )
        memory_note.setStyleSheet("QLabel { color: #666; }")
        memory_layout.addWidget(memory_note)

        memory_group.setLayout(memory_layout)
        layout.addWidget(memory_group)

        layout.addStretch()
        self.setLayout(layout)

        # Register fields for later access
        self.registerField("wifi_camera_enabled", self.use_wifi_camera)
        self.registerField("tapo_host*", self.tapo_host)
        self.registerField("tapo_username*", self.tapo_username)
        self.registerField("tapo_password*", self.tapo_password)
        self.registerField("usb_camera_enabled", self.use_usb_camera)
        self.registerField("memory_enabled", self.use_memory)

    def _on_wifi_camera_changed(self, state):
        """Enable/disable WiFi camera form"""
        self.wifi_form.setEnabled(state == Qt.CheckState.Checked.value)

    def _on_usb_camera_changed(self, state):
        """Enable/disable USB camera list"""
        enabled = state == Qt.CheckState.Checked.value
        self.usb_camera_list.setEnabled(enabled)
        if enabled:
            self._scan_usb_cameras()

    def _scan_usb_cameras(self):
        """Scan for USB cameras"""
        self.usb_camera_list.clear()

        try:
            import cv2
            # Try to open cameras 0-9
            found_cameras = []
            for i in range(10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    found_cameras.append(f"Camera {i}")
                    cap.release()

            if found_cameras:
                for camera in found_cameras:
                    item = QListWidgetItem(f"✅ {camera}")
                    self.usb_camera_list.addItem(item)
            else:
                item = QListWidgetItem("No USB cameras found")
                item.setForeground(Qt.GlobalColor.gray)
                self.usb_camera_list.addItem(item)

        except ImportError:
            item = QListWidgetItem("⚠️ OpenCV not installed")
            item.setForeground(Qt.GlobalColor.red)
            self.usb_camera_list.addItem(item)

    def isComplete(self):
        """Page is complete if at least one camera is selected with valid config"""
        if self.use_wifi_camera.isChecked():
            # WiFi camera requires host, username, password
            if not (
                self.tapo_host.text().strip()
                and self.tapo_username.text().strip()
                and self.tapo_password.text().strip()
            ):
                return False

        # At least one camera must be selected
        return self.use_wifi_camera.isChecked() or self.use_usb_camera.isChecked()
