"""Completion page"""
from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QTextBrowser,
)
from PyQt6.QtCore import Qt


class CompletePage(QWizardPage):
    """Installation complete page"""

    def __init__(self):
        super().__init__()
        self.setTitle("Installation Complete!")
        self.setSubTitle("Embodied Claude is ready to use")

        layout = QVBoxLayout()

        # Success message
        success_label = QLabel("✅ Installation completed successfully!")
        success_label.setStyleSheet(
            "QLabel { color: green; font-size: 16px; font-weight: bold; }"
        )
        layout.addWidget(success_label)

        # Next steps
        next_steps = QTextBrowser()
        next_steps.setOpenExternalLinks(True)
        next_steps.setHtml(
            """
            <h3>Next Steps</h3>

            <ol>
                <li><strong>Restart Claude Code</strong> to load the new MCP servers</li>
                <li><strong>Test your setup:</strong>
                    <ul>
                        <li>"今何が見える？" (What do you see now?)</li>
                        <li>"左を見て" (Look left)</li>
                        <li>"何か聞こえる？" (Do you hear anything?)</li>
                        <li>"これ覚えておいて：..." (Remember this: ...)</li>
                    </ul>
                </li>
                <li><strong>Check the documentation:</strong>
                    <a href="https://github.com/kmizu/embodied-claude">
                    GitHub Repository
                    </a>
                </li>
            </ol>

            <h3>Installed MCP Servers</h3>
            <p>Your Claude Code now has access to:</p>
            <ul>
                <li><strong>wifi-cam</strong> - Eyes, neck, ears (Wi-Fi camera)</li>
                <li><strong>memory</strong> - Long-term memory (ChromaDB)</li>
                <li><strong>system-temperature</strong> - Body temperature sense</li>
            </ul>

            <h3>Troubleshooting</h3>
            <p>If you encounter issues:</p>
            <ul>
                <li>Check <code>~/.claude/settings.json</code> for MCP configuration</li>
                <li>View logs with <code>claude --verbose</code></li>
                <li>Report issues on
                    <a href="https://github.com/kmizu/embodied-claude/issues">
                    GitHub Issues
                    </a>
                </li>
            </ul>

            <h3>Optional: Autonomous Action</h3>
            <p>
                To enable periodic autonomous observation (every 10 minutes),
                see the README section on "Autonomous Action Script".
            </p>
            """
        )
        layout.addWidget(next_steps)

        self.setLayout(layout)
