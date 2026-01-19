from typing import Any, Optional
from PySide6.QtCore import QObject, QSettings, Signal
from qfluentwidgets import OptionsConfigItem, OptionsValidator, EnumSerializer, Theme

class UserSettingItem(OptionsConfigItem):
    
    def serialization_key(self) -> str:
        return f"{self.group}/{self.key}"

class UserSettings(QObject):
    organization: str = "imharryzhu"
    application: str = "MyGreateApp"

    appTheme: UserSettingItem

    valueChanged = Signal(str, object)

    _instance: Optional['UserSettings'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserSettings, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, user: str, parent: Optional[QObject] = None):
        if cls._instance is None:
            cls.application = f"MyGreateApp_{user}"
        return cls(parent)

    def __init__(self, parent: Optional[QObject] = None ):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        super().__init__(parent)
        self._settings = QSettings(self.organization, self.application)
        self._initialized = True

        self._create_theme_setting()

    def _create_theme_setting(self):
        self.appTheme = UserSettingItem(
            "MyGreateApp", 
            "AppTheme", 
            Theme.AUTO, 
            OptionsValidator(Theme), 
            EnumSerializer(Theme))
        serialization_key = self.appTheme.serialization_key()
        stored_value = self.get(serialization_key, Theme.AUTO, Theme)
        self.appTheme.value = stored_value
        self.appTheme.valueChanged.connect(
            lambda value: self.set(serialization_key, value)
        )
    
    def get(self, key: str, default: Any = None, value_type: type | None = None) -> Any:
        """获取配置值并转换为指定类型
        
        Args:
            key: 配置键
            default: 默认值
            value_type: 目标类型（支持 bool、枚举等特殊类型）
            
        Returns:
            转换后的配置值，转换失败时返回默认值
        """
        value = self._settings.value(key, default)

        # 如果不需要类型转换，或值为 None，直接返回
        if value_type is None or value is None:
            return value
        
        # 如果已经是目标类型，直接返回
        if isinstance(value, value_type):
            return value

        try:
            # 特殊处理 bool 类型（避免 bool('false') 返回 True）
            if value_type is bool:
                if isinstance(value, str):
                    return value.lower() in ('true', '1', 'yes')
                return bool(value)
            
            # 特殊处理枚举类型
            if hasattr(value_type, '__members__'):  # 是枚举类型
                # QSettings 可能返回枚举的 name（字符串）或 value（整数）
                if isinstance(value, str):
                    # 尝试通过名称获取（如 "AUTO"）
                    if value in value_type.__members__:
                        return value_type[value]
                    # 尝试去掉前缀（如 "Theme.AUTO" -> "AUTO"）
                    simple_name = value.split('.')[-1]
                    if simple_name in value_type.__members__:
                        return value_type[simple_name]
                # 尝试通过值获取
                return value_type(value)
            
            # 其他类型直接转换
            return value_type(value)
            
        except (ValueError, TypeError, KeyError) as e:
            # 类型转换失败时返回默认值
            return default

    def set(self, key: str, value: Any) -> None:
        self._settings.setValue(key, value)
        self.valueChanged.emit(key, value)

    def remove(self, key: str) -> None:
        self._settings.remove(key)
        self.valueChanged.emit(key, None)

    def contains(self, key: str) -> bool:
        return self._settings.contains(key)

    def clear(self) -> None:
        self._settings.clear()

    def sync(self) -> None:
        self._settings.sync()

    def begin_group(self, group: str):
        self._settings.beginGroup(group)

    def end_group(self):
        self._settings.endGroup()
