from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        # Return the label as the root widget
        return Label(text='Hello, world!')

if __name__ == '__main__':
    TestApp().run()
