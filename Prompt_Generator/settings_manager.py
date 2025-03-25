# settings_manager.py

from PyQt6.QtCore import QSettings

class SettingsManager:
    def __init__(self, org_name, app_name):
        self.settings = QSettings(org_name, app_name)

    def save_setting(self, key, value):
        self.settings.setValue(key, value)

    def load_setting(self, key, default_value):
        return self.settings.value(key, default_value)