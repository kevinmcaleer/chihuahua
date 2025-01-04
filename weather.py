import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
import os
import requests

class WeatherWidget(BoxLayout):
    city = StringProperty("London")  # Default city
    api_key = StringProperty("")     # OpenWeatherMap API key
    temperature = NumericProperty(0)  # Current temperature
    icon_url = StringProperty("")    # URL for the weather icon
    temperature_font_size = NumericProperty(120)  # Default font size for time

    def __init__(self, **kwargs):
        super(WeatherWidget, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = 10
        self.spacing = 10

        # Add UI components
        self.label = Label(text="Fetching weather...", size_hint=(1, 1), font_size=80, halign="left")
        self.icon = Image(size_hint=(None, None))  # Weather icon
        # self.icon.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        
        grid = GridLayout(cols=2, spacing=10, padding=10)
        grid.add_widget(self.icon)
        grid.add_widget(self.label)
        self.add_widget(grid)

        # Fetch weather on initialization and every 10 minutes
        self.fetch_weather()
        Clock.schedule_interval(lambda dt: self.fetch_weather(), 600)

        self.bind(size=self.update_temp_size)

    def on_api_key(self, instance, value):
        """Triggered when the api_key property changes."""
        Logger.info(f"API Key updated to: {value}")
        print(f"API Key updated to: {value}")
        self.fetch_weather()

    def on_city(self, instance, value):
        """Triggered when the city property changes."""
        Logger.info(f"City updated to: {value}")
        print(f"City updated to: {value}")
        self.fetch_weather()    

    def fetch_weather(self):
        """Fetch current weather data from OpenWeatherMap."""
        if not self.api_key:
            Logger.error("WeatherWidget: API key is missing!")
            self.label.text = "Missing API Key"
            return

        try:
            # OpenWeatherMap API endpoint
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
            # print(f'url: {url}')
            response = requests.get(url)
            # print(f'response: {response}')
            if response.status_code == 200:
                data = response.json()
                self.temperature = data["main"]["temp"]
                icon_code = data["weather"][0]["icon"]
                self.icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                print(f"Temperature: {self.temperature}°C")
                # Update UI
                self.update_ui()
            else:
                Logger.error(f"WeatherWidget: Failed to fetch weather data - {response.status_code}")
                self.label.text = "Error fetching weather"
        except Exception as e:
            Logger.error(f"WeatherWidget: Exception occurred - {e}")
            self.label.text = "Error fetching weather"

    def update_ui(self):
        """Update the UI with the current temperature and icon."""
        self.label.text = f"{self.temperature}°C"
        self.label.x = 0
        self.label.y = 0

        # Download the weather icon locally
        icon_filename = "weather_icon.png"  # Temporary file to store the icon
        try:
            response = requests.get(self.icon_url, stream=True)
            if response.status_code == 200:
                # Save the image locally
                with open(icon_filename, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                self.icon.source = icon_filename  # Set the local file as the image source
            else:
                Logger.error(f"WeatherWidget: Failed to fetch weather icon - {response.status_code}")
                self.icon.source = "default_icon.png"  # Set a fallback icon
        except Exception as e:
            Logger.error(f"WeatherWidget: Exception occurred while fetching icon - {e}")
            self.icon.source = "default_icon.png"  # Set a fallback icon

    def update_temp_size(self, *args):
        """Update font size and icon size dynamically."""
        if self.label:
            self.label.font_size = self.width * 0.1
        if self.icon:
            self.icon.size = (self.width * 0.3, self.height * 0.3)  # Scale icon size dynamically
