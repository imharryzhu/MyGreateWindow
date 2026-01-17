from enum import Enum
from qfluentwidgets import FluentIconBase, Theme, getIconColor

class CustomIcon(FluentIconBase, Enum):

    IKUN = 'ikun'

    def path(self, theme=Theme.AUTO):
        return f':/icons/{self.value}_{getIconColor(theme)}.svg'
