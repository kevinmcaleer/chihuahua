import feedparser
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.logger import Logger
import logging
from rounded import RoundedRectangleContainer
from kivy.uix.gridlayout import GridLayout

Logger.setLevel(logging.INFO)  # Set the log level to INFO

class NewsWidget(BoxLayout):
    rss_url = StringProperty("https://rss.cnn.com/rss/edition.rss")  # Default RSS feed URL
    headlines = ListProperty([])  # List to store fetched headlines
    

    def __init__(self, **kwargs):
        super(NewsWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        print(f"Fetching news from {self.rss_url}")


    def on_rss_url(self, instance, value):
        """Triggered when the rss_url property changes."""
        Logger.info(f"RSS URL updated to: {value}")
        self.fetch_headlines()

    def fetch_headlines(self):
        """Fetch news headlines from the RSS feed."""
        try:
            feed = feedparser.parse(self.rss_url)
            # feed = feedparser.parse(self.rss_url, request_kwargs={'verify': False})

            # print(f"Feed: {feed}")
            self.headlines = [entry.title for entry in feed.entries[:5]]  # Get top 5 headlines
            Logger.info(f"Fetched {len(self.headlines)} headlines from {self.rss_url}")
            print(self.headlines)
            self.update_headlines()
        except Exception as e:
            Logger.error(f"Failed to fetch news: {e}")
            self.headlines = ["Error fetching news"]
            self.update_headlines()

    def update_headlines(self):
        """Update the widget with the latest headlines."""
        self.clear_widgets()  # Clear existing widgets

        for headline in self.headlines:
            label = Label(text=headline, size_hint_y=None, height=50, halign="left", valign="middle")
            label.bind(size=label.setter('text_size'))  # Proper alignment
            label.color = (1, 1, 1, 1)  # White text color

            # Add a background color to the label using Canvas
            with label.canvas.before:
                Color(0.2, 0.2, 0.2, 1)  # Dark grey background
                Rectangle(size=label.size, pos=label.pos)
                # label.bind(size=lambda instance, value: setattr(instance.canvas.before.children[0], 'size', value))
                # label.bind(pos=lambda instance, value: setattr(instance.canvas.before.children[0], 'pos', value))

            self.add_widget(label)
        
