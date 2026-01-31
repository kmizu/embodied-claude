"""API key configuration page"""
from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextBrowser,
    QFormLayout,
)
from PyQt6.QtCore import Qt


class ApiKeyPage(QWizardPage):
    """Configure Claude API key"""

    def __init__(self):
        super().__init__()
        self.setTitle("Claude API Key")
        self.setSubTitle("Enter your Anthropic API key")

        layout = QVBoxLayout()

        # Instructions
        instructions = QTextBrowser()
        instructions.setOpenExternalLinks(True)
        instructions.setMaximumHeight(150)
        instructions.setHtml(
            """
            <p>
                To use Claude Code with Embodied Claude, you need an Anthropic API key.
            </p>
            <ul>
                <li>Get your API key from:
                <a href="https://console.anthropic.com/settings/keys">
                Anthropic Console
                </a></li>
                <li>Or skip this if you already configured it in Claude Code</li>
            </ul>
            """
        )
        layout.addWidget(instructions)

        # API key input
        form_layout = QFormLayout()

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-ant-api03-...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("API Key:", self.api_key_input)

        layout.addLayout(form_layout)

        # Note
        note = QLabel(
            "💡 Your API key will be stored in Claude Code's configuration.\n"
            "It will NOT be stored in the embodied-claude repository."
        )
        note.setWordWrap(True)
        note.setStyleSheet("QLabel { color: #666; margin-top: 10px; }")
        layout.addWidget(note)

        layout.addStretch()
        self.setLayout(layout)

        # Register field (not required - user might skip)
        self.registerField("api_key", self.api_key_input)
