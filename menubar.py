# menutext.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty

class MenuBar(BoxLayout):
    height = NumericProperty(100)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"  # Horizontal layout
        self.size_hint_y = None          # Fix the height of the menu bar
        
        # Add menu buttons
        self.add_widget(Button(text="File", on_press=self.on_file))
        self.add_widget(Button(text="Edit", on_press=self.on_edit))
        self.add_widget(Button(text="View", on_press=self.on_view))
        self.add_widget(Button(text="Help", on_press=self.on_help))

    def on_file(self, instance):
        print("File menu clicked")

    def on_edit(self, instance):
        print("Edit menu clicked")

    def on_view(self, instance):
        print("View menu clicked")

    def on_help(self, instance):
        print("Help menu clicked")
