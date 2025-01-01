from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class MyWidget(Widget):

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.background_image = None
        self.rect = None
        self.init_background_image()
        self.init_shapes()

    def init_background_image(self):
        with self.canvas:
            self.background_image = Rectangle(source='background.jpg', pos=self.pos, size=self.size)

    def init_shapes(self):
        with self.canvas:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(pos=(0, 0), size=(self.width / 2, self.height / 2))

    def adjust_background_image(self):
        # Calculate the aspect ratio of the widget and the image
        widget_aspect = self.width / self.height
        image_width, image_height = self.background_image.texture.size
        image_aspect = image_width / image_height

        if widget_aspect > image_aspect:
            # Widget is wider than the image
            new_width = self.width
            new_height = self.width / image_aspect
        else:
            # Widget is taller than the image
            new_width = self.height * image_aspect
            new_height = self.height

        # Center the image
        self.background_image.size = (new_width, new_height)
        self.background_image.pos = (
            (self.width - new_width) / 2,
            (self.height - new_height) / 2
        )

    def on_size(self, *args):
        # Update the size and position of canvas elements when the window resizes
        if self.background_image:
            self.adjust_background_image()
        if self.rect:
            self.rect.pos = (0, 0)
            self.rect.size = (self.width / 2, self.height / 2)


class MyApp(App):
    def build(self):
        return MyWidget()
    
if __name__ == '__main__':
    MyApp().run()
