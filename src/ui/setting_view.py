from typing import Union
from PySide6.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QLabel,
    QButtonGroup
)
from PySide6.QtCore import (
    Signal,
    Qt
)
from PySide6.QtGui import QIcon

from qfluentwidgets import (
    ScrollArea,
    ExpandLayout,
    SettingCardGroup,
    SettingCard,
    FluentIcon,
    PushButton,
    StrongBodyLabel,
    Theme,
    RadioButton,
    ExpandSettingCard,
    OptionsConfigItem,
    FluentIconBase,
    setTheme
)

from core.user_settings import UserSettings
from resources.custom_icon import CustomIcon

class UserSettingCard(ExpandSettingCard):
    """
    抄袭 qfluentwidgets 的 OptionsSettingCard，主要为了用QSettings作为存储介质
    """

    optionChanged = Signal(OptionsConfigItem)

    def __init__(self, configItem, icon: Union[str, QIcon, FluentIconBase], title, content=None, texts=None, parent=None):
        """
        Parameters
        ----------
        configItem: OptionsConfigItem
            options config item

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of setting card

        content: str
            the content of setting card

        texts: List[str]
            the texts of radio buttons

        parent: QWidget
            parent window
        """
        super().__init__(icon, title, content, parent)
        self.texts = texts or []
        self.configItem = configItem
        self.configName = configItem.name
        self.choiceLabel = QLabel(self)
        self.buttonGroup = QButtonGroup(self)

        self.choiceLabel.setObjectName("titleLabel")
        self.addWidget(self.choiceLabel)

        # create buttons
        self.viewLayout.setSpacing(19)
        self.viewLayout.setContentsMargins(48, 18, 0, 18)
        for text, option in zip(texts, configItem.options):
            button = RadioButton(text, self.view)
            self.buttonGroup.addButton(button)
            self.viewLayout.addWidget(button)
            button.setProperty(self.configName, option)

        self._adjustViewSize()
        self.setValue(UserSettings().get(self.configItem.serialization_key()))
        configItem.valueChanged.connect(self.setValue)
        self.buttonGroup.buttonClicked.connect(self.__onButtonClicked)

    def __onButtonClicked(self, button: RadioButton):
        """ button clicked slot """
        if button.text() == self.choiceLabel.text():
            return

        value = button.property(self.configName)
        # 通过设置 configItem.value 触发 valueChanged 信号
        self.configItem.value = value

        self.choiceLabel.setText(button.text())
        self.choiceLabel.adjustSize()
        self.optionChanged.emit(self.configItem)

    def setValue(self, value):
        """ select button according to the value """
        for button in self.buttonGroup.buttons():
            isChecked = button.property(self.configName) == value
            button.setChecked(isChecked)

            if isChecked:
                self.choiceLabel.setText(button.text())
                self.choiceLabel.adjustSize()

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

        self._initUICard()
        self._initAboutCard()
        self._initWidget()
    
    def _initUICard(self):
        # region UI设置
        self.userUIGroup = SettingCardGroup("UI", self.scrollWidget)
        self.appTheme = UserSettingCard(
            UserSettings().appTheme,
            FluentIcon.PALETTE,
            '主题颜色',
            texts=[
                Theme.LIGHT.value,
                Theme.DARK.value,
                Theme.AUTO.value
            ],
            parent=self.userUIGroup
        )
        UserSettings().appTheme.valueChanged.connect(self.onThemeChanged)
        self.userUIGroup.addSettingCard(self.appTheme)
        self.expandLayout.addWidget(self.userUIGroup)

        # endregion

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

    def onThemeChanged(self, theme: Theme):
        setTheme(theme)
