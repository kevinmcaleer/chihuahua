from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from clock import ClockWidget
from chart import ChartWidget
from gauge import Gauge
from news import NewsWidget
from kivy.logger import Logger
import logging

Logger.setLevel(level='INFO')  # Set the log level to INFO
logging.basicConfig(level=logging.WARNING)

import kivy

# Set Kivy log level
kivy.config.Config.set('kivy', 'log_level', 'warning')  # Suppress debug messages
kivy.config.Config.write()

# Declare screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class TestScreen(Screen):
    pass

class WeatherScreen(Screen):
    pass

class TestApp(App):

    def build(self):
        # Load the .kv file
        Builder.load_file('app.kv')

        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(TestScreen(name='test'))
        sm.add_widget(WeatherScreen(name='weather'))

        return sm

if __name__ == '__main__':
    TestApp().run()