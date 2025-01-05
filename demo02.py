from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


# Define the first screen
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Go to Second Screen', on_press=self.go_to_second_screen))
        self.add_widget(layout)

    def go_to_second_screen(self, instance):
        self.manager.current = 'second'  # Switch to the second screen


# Define the second screen
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Go Back to First Screen', on_press=self.go_back))
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'first'  # Switch back to the first screen


# Define the ScreenManager and add screens
class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))  # Add the first screen
        sm.add_widget(SecondScreen(name='second'))  # Add the second screen
        return sm


if __name__ == '__main__':
    TestApp().run()
