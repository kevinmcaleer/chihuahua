from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from clock import ClockWidget
from chart import ChartWidget
from gauge import Gauge
from news import NewsWidget
from kivy.logger import Logger
from weather import WeatherWidget
from menubar import MenuBar
import logging
from kivy.uix.widget import Widget
from kivy.graphics import RoundedRectangle, Color
from rounded import RoundedRectangleContainer

Logger.setLevel(level='INFO')  # Set the log level to INFO
logging.basicConfig(level=logging.WARNING)

import kivy

# Set Kivy log level
kivy.config.Config.set('kivy', 'log_level', 'warning')  # Suppress debug messages
kivy.config.Config.write()
kivy.config.Config.set('graphics', 'borderless', '1')
kivy.config.Config.set('graphics', 'fullscreen', '0')
kivy.config.Config.write()


# Declare screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class NewsScreen(Screen):
    pass

class WeatherScreen(Screen):
    pass

class SmartHomeScreen(Screen):
    pass

class RoundedButton(Widget):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint = (1, 1)  # Adjust size_hint as needed
        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 1)  # Blue background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class TestApp(App):

    def build(self):
        # Load the .kv file
        Builder.load_file('app.kv')

        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(NewsScreen(name='news'))
        sm.add_widget(WeatherScreen(name='weather'))
        sm.add_widget(SmartHomeScreen(name='smarthome'))

        return sm

if __name__ == '__main__':
    TestApp().run()