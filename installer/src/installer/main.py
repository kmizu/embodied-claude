"""
Embodied Claude Installer
GUI installer for setting up Embodied Claude MCP servers
"""
import sys
from PyQt6.QtWidgets import QApplication, QWizard
from PyQt6.QtCore import Qt

from .pages.welcome import WelcomePage
from .pages.dependencies import DependenciesPage
from .pages.camera import CameraSelectionPage
from .pages.api_key import ApiKeyPage
from .pages.install import InstallationPage
from .pages.complete import CompletePage


class EmbodiedClaudeInstaller(QWizard):
    """Main installer wizard"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Embodied Claude Installer")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setOption(QWizard.WizardOption.HaveHelpButton, False)
        self.setMinimumSize(800, 600)

        # Add pages
        self.addPage(WelcomePage())
        self.addPage(DependenciesPage())
        self.addPage(CameraSelectionPage())
        self.addPage(ApiKeyPage())
        self.addPage(InstallationPage())
        self.addPage(CompletePage())


def main():
    """Entry point for the installer"""
    app = QApplication(sys.argv)
    app.setApplicationName("Embodied Claude Installer")

    wizard = EmbodiedClaudeInstaller()
    wizard.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
