from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from clock import ClockWidget
from chart import ChartWidget

# Declare screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class TestScreen(Screen):
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

        return sm

if __name__ == '__main__':
    TestApp().run()