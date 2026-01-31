"""Welcome page for the installer wizard"""
from PyQt6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QTextBrowser,
)
from PyQt6.QtCore import Qt


class WelcomePage(QWizardPage):
    """Welcome page with project introduction"""

    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to Embodied Claude")
        self.setSubTitle(
            "Give Claude physical senses: eyes, ears, and long-term memory"
        )

        layout = QVBoxLayout()

        # Project description
        description = QTextBrowser()
        description.setOpenExternalLinks(True)
        description.setMaximumHeight(400)
        description.setHtml(
            """
            <h2>AIに身体を与えるプロジェクト</h2>
            <p>
                Embodied Claude は、安価なハードウェア（約4,000円）で Claude に
                「目」「首」「耳」「脳（長期記憶）」を与える MCP サーバー群です。
            </p>

            <h3>コンセプト</h3>
            <blockquote>
                「AIに身体を」と聞くと高価なロボットを想像しがちですが、
                <strong>3,980円のWi-Fiカメラで目と首は十分実現できます</strong>。
                本質（見る・動かす）だけ抽出したシンプルさが特徴です。
            </blockquote>

            <h3>このインストーラでセットアップされるもの</h3>
            <ul>
                <li><strong>目（Eye）</strong>: USB/Wi-Fi カメラで視覚を獲得</li>
                <li><strong>首（Neck）</strong>: PTZ カメラで見たい方向を向ける</li>
                <li><strong>耳（Ear）</strong>: マイクで音声を聞き取る（Whisper）</li>
                <li><strong>脳（Brain）</strong>: 長期記憶（ChromaDB）</li>
            </ul>

            <h3>必要なハードウェア</h3>
            <ul>
                <li>Wi-Fi PTZ カメラ（推奨: TP-Link Tapo C210/C220 - 約3,980円）</li>
                <li>GPU（Whisper 音声認識用、オプション）</li>
            </ul>

            <p>
                <a href="https://github.com/kmizu/embodied-claude">
                GitHub リポジトリ
                </a>
            </p>
            """
        )
        layout.addWidget(description)

        # Note
        note = QLabel(
            "⚠️ このインストーラは Claude Code の MCP 設定を自動生成します。\n"
            "既存の設定は上書きされませんが、バックアップを推奨します。"
        )
        note.setWordWrap(True)
        note.setStyleSheet("QLabel { color: #666; margin-top: 10px; }")
        layout.addWidget(note)

        self.setLayout(layout)
