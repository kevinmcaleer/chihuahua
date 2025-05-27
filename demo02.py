from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from clock import ClockWidget
from news import NewsWidget
from chart import ChartWidget

# Define the first screen
class FirstScreen(Screen):
    pass


# Define the second screen
class SecondScreen(Screen):
    pass

class ThirdScreen(Screen):
    pass

# Define the ScreenManager and add screens
class TestApp(App):
    def build(self):
        # Load the .kv file
        Builder.load_file('live.kv')

        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))  # Add the first screen
        sm.add_widget(SecondScreen(name='second'))  # Add the second screen
        sm.add_widget(ThirdScreen(name='third'))
        return sm


if __name__ == '__main__':
    TestApp().run()
