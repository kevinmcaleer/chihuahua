from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from datetime import datetime

class ClockWidget(BoxLayout):

    time_font_size = NumericProperty(120)  # Default font size for time
    date_font_size = NumericProperty(80)  # Default font size for date
    time_label = ObjectProperty(None)     # Reference to the time label
    date_label = ObjectProperty(None)     # Reference to the date label

    def __init__(self, **kwargs):
        super(ClockWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'  # Arrange the clock vertically
        self.padding = 20
        self.spacing = 10

         # Add a label to display the time
        self.time_label = Label(font_size=self.time_font_size, halign="center", valign="middle")
        self.time_label.bind(size=self.time_label.setter('text_size'))  # Ensure proper alignment
        self.add_widget(self.time_label)

        # Add a label to display the date
        self.date_label = Label(font_size=self.date_font_size, halign="center", valign="middle")
        self.date_label.bind(size=self.date_label.setter('text_size'))  # Ensure proper alignment
        self.add_widget(self.date_label)

      

        # Schedule the time update to happen every second
        Clock.schedule_interval(self.update_time, 1)  # Update every second
        self.update_time()  # Initial update

    def update_time(self, *args):
        """Update the time and date."""
        current_time = datetime.now()
        self.time_label.text = current_time.strftime("%H:%M:%S")
        self.date_label.text = current_time.strftime("%A, %B %d, %Y")

    # def set_font_sizes(self, time_font_size, date_font_size):
    #     """Update the font sizes for the time and date labels."""
    #     self.time_label.font_size = time_font_size
    #     self.date_label.font_size = date_font_size
