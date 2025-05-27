from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class FirstScreen(Screen):
    """ First screen of the application """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Go to Second Screen', on_press=self.go_to_second_screen))

    def go_to_second_screen(self, instance):
        self.manager.current = 'second' # Switch to the second screen

class SecondScreen(Screen):
    """ Second screen of the application """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Go Back to First Screen', on_press=self.go_back))
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'first' # Switch back to the first screen


class TestApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        return sm
    

if __name__ == '__main__':
    TestApp().run()