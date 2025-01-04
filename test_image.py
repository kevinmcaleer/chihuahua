from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

class TestScreen(Screen):
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.add_widget(Image(source='background.jpg'))  # Add the image widget to the screen

class TestApp(App):
    def build(self):
        sm = ScreenManager()  # Create a ScreenManager instance
        test_screen = TestScreen(name='test_screen')  # Instantiate TestScreen with a name
        sm.add_widget(test_screen)  # Add the TestScreen to the ScreenManager
        return sm  # Return the ScreenManager as the root widget

# Run the app
if __name__ == '__main__':
    TestApp().run()
