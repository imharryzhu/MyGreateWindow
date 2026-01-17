from typing import Union
from PySide6.QtGui import QIcon
from PySide6.QtCore import QPoint
from qfluentwidgets import (
    FluentWindow,
    SystemThemeListener,
    FluentIcon,
    NavigationItemPosition,
    RoundMenu,
    Theme,
    setTheme
)

from resources.custom_icon import CustomIcon
from ui.setting_view import SettingView

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self._initWindow()

        setTheme(Theme.LIGHT, save=False)

        # create system theme listener
        self.themeListener = SystemThemeListener()

        # enable arcylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.navigationInterface.setReturnButtonVisible(False)

        self._initNavigation()

    def _initWindow(self):
        self.resize(800, 600)
        self.setWindowTitle('My Great Window')
        self.setWindowIcon(CustomIcon.IKUN.icon())

        desktop = self.screen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def _initNavigation(self):

        self.navigationInterface.addSeparator()

        self.settingView = SettingView(self)

        self.addSubInterface(self.settingView, 
                             FluentIcon.SETTING, 
                             'Settings', 
                             NavigationItemPosition.BOTTOM)
        
    def addSubMenuInterface(self, 
                            roundMenu: RoundMenu, 
                            icon: Union[FluentIcon, QIcon], 
                            text: str, 
                            position: NavigationItemPosition):
        
        item = self.navigationInterface.addItem(
            routeKey=text.lower(),
            icon=icon,
            text=text,
            onClick=None,
            selectable=False,
            position=position
        )

        def onItemClicked():
            rect = item.rect()
            centerRight = QPoint(rect.right(), rect.center().y())
            roundMenu.exec(item.mapToGlobal(centerRight))

        item.clicked.connect(onItemClicked)

