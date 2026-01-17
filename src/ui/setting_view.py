from PySide6.QtWidgets import (
    QWidget, 
    QHBoxLayout
)
from PySide6.QtCore import Qt
from qfluentwidgets import (
    ScrollArea,
    ExpandLayout,
    SettingCardGroup,
    SettingCard,
    FluentIcon,
    PushButton,
    StrongBodyLabel
)

from resources.custom_icon import CustomIcon

class SettingView(ScrollArea):

    def __init__(self, parent = None):
        super().__init__(parent)

        self._initUI()

    def _initUI(self):

        self.setObjectName('SettingView')
        self.setStyleSheet('border: none; background-color: transparent;')

        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName('SettingScrollWidget')
        self.scrollWidget.setStyleSheet('border: none; background-color: transparent;')

        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 15, 60, 0)

        self._initAboutCard()
        self._initWidget()

    def _initAboutCard(self):
        self.aboutGroup = SettingCardGroup('About', self.scrollWidget)

        # region thanks
        thanksCard = SettingCard(FluentIcon.FEEDBACK, '感谢支持', '', self.aboutGroup)
        thanksCard.hBoxLayout.addStretch(1)

        thanksWidget = QWidget()
        thanksLayout = QHBoxLayout(thanksWidget)
        thanksLayout.setContentsMargins(0, 0, 16, 0)
        thanksLayout.setSpacing(10)

        likeButton = PushButton(CustomIcon.IKUN, '点赞')
        likeButton.setCheckable(False)
        # likeButton.clicked.connect(lambda: print('点赞'))

        thanksLayout.addWidget(likeButton)
        thanksCard.hBoxLayout.addWidget(thanksWidget)
        self.aboutGroup.addSettingCard(thanksCard)
        # endregion

        # region 
        versionCard = SettingCard(FluentIcon.INFO, '版本信息', '', self.aboutGroup)
        versionCard.hBoxLayout.addStretch(1)

        versionWidget = QWidget()
        versionLayout = QHBoxLayout(versionWidget)
        versionLayout.setContentsMargins(0, 0, 16, 0)
        versionLayout.setSpacing(4)

        versionLabel = StrongBodyLabel('当前版本: 0.0.1')
        versionLabel.setAlignment(Qt.AlignmentFlag.AlignRight)

        versionLayout.addWidget(versionLabel)
        versionCard.hBoxLayout.addWidget(versionWidget)
        self.aboutGroup.addSettingCard(versionCard)
        # endregion

        self.expandLayout.addWidget(self.aboutGroup)

    def _initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
