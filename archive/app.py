from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from clock import ClockWidget  # Import ClockWidget from the separate file

class MyWidget(BoxLayout):  # Change to BoxLayout to support layout widgets
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        self.background_image = None
        self.init_background_image()

        # Add clock widget
        clock_widget = ClockWidget()
        self.add_widget(clock_widget)

        # Add other widgets here
        self.init_close_icon()

    def init_background_image(self):
        with self.canvas.before:  # Draw the background before other widgets
            self.background_image = Rectangle(source='background.jpg', pos=self.pos, size=self.size)

    def init_close_icon(self):
        # Create a close icon
        self.close_icon = Label(
            text="X", font_size=20, size_hint=(None, None), size=(30, 30), pos_hint={"right": 1, "top": 1}
        )
        self.add_widget(self.close_icon)

    def on_size(self, *args):
        # Adjust background image size
        if self.background_image:
            self.background_image.size = self.size
            self.background_image.pos = self.pos


class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()
