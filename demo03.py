# Demo 3
# Also create demo.kv file

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Define the first screen
class FirstScreen(Screen):
    pass


# Define the second screen
class SecondScreen(Screen):
    pass


# Define the ScreenManager and add screens
class TestApp(App):

    def build(self):
        # Load the .kv file
        Builder.load_file('demo.kv')

        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
 
        return sm


if __name__ == '__main__':
    TestApp().run()
