import paho.mqtt.client as mqtt
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.logger import Logger
from kivy.clock import Clock
Logger.setLevel("ERROR")
import matplotlib.pyplot as plt
import logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

from kivy.graphics import Color, Rectangle

class ChartWidget(BoxLayout):
    mqtt_server = StringProperty("192.168.1.152")  # MQTT broker address
    mqtt_topic = StringProperty("/home/loft")  # Default MQTT topic
    min_range = NumericProperty(0)            # Min range for y-axis
    max_range = NumericProperty(100)          # Max range for y-axis
    data_points = ListProperty([])            # List to store incoming values
    background_color = ListProperty([0.1, 0.5, 0.8, 1])  # Default background color (blue)
    title = StringProperty("Real-time Data")  # Chart title

    def __init__(self, **kwargs):
        super(ChartWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        # Add a background color to the widget
        with self.canvas.before:
            self.bg_color = Color(*self.background_color)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)
        self.bind(background_color=self.update_color)
        self.bind(title=self.update_title)

        # Initialize the matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_alpha(0)  # Transparent figure background
        self.ax.set_facecolor((0, 0, 0, 0))

        self.ax.set_ylim(self.min_range, self.max_range)
        self.ax.set_title("Real-time Data")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")

        # Add the matplotlib canvas to the Kivy widget
        self.canvas_widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(self.canvas_widget)

        # Connect to MQTT broker
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect(self.mqtt_server, 1883)  # Update with your broker details
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            Logger.error(f"Failed to connect to MQTT broker: {e}")
        self.client.loop_start()

    def _update_bg_rect(self, *args):
        """Update the size and position of the background rectangle."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def update_color(self, *args):
        """Update the background color dynamically."""
        self.bg_color.rgba = self.background_color

    def on_connect(self, client, userdata, flags, rc):
        """Callback when the MQTT client connects."""
        if rc == 0:
            print(f"Connected to MQTT broker, subscribing to {self.mqtt_topic}")
            Logger.info(f"Connected to MQTT broker, subscribing to {self.mqtt_topic}")
            client.subscribe(self.mqtt_topic)
        else:
            print("Failed to connect to MQTT broker")
            Logger.error("Failed to connect to MQTT broker")

    def on_mqtt_topic(self, instance, value):
        """Callback when the MQTT topic changes."""
        self.client.unsubscribe(self.mqtt_topic)
        self.client.subscribe(value)
        print(f"Changed MQTT topic to {value}")
        Logger.info(f"Changed MQTT topic to {value}")

    def on_min_range(self, instance, value):
        """Callback when the min range changes."""
        self.ax.set_ylim(value, self.max_range)
        self.update_plot()

    def on_max_range(self, instance, value):
        """Callback when the max range changes."""
        self.ax.set_ylim(self.min_range, value)
        self.update_plot()

    def on_message(self, client, userdata, msg):
        """Callback for receiving a message."""
        try:
            value = float(msg.payload.decode("utf-8"))
            self.data_points.append(value)

            # Keep only the last 100 data points
            self.data_points = self.data_points[-100:]

            # Schedule the plot update on the main Kivy thread
            Clock.schedule_once(lambda dt: self.update_plot())
        except ValueError:
            print("Invalid payload received, expected a float")

    def update_plot(self):
        """Update the chart with new data."""
        self.ax.clear()
        self.ax.set_facecolor((0, 0, 0, 0))  # Ensure transparent axes background
        self.ax.set_ylim(self.min_range, self.max_range)

        # Plot the data with a white line
        self.ax.plot(self.data_points, label="MQTT Data", color="white")

        # Set title and labels with white font
        self.ax.set_title(self.title, color="white")  # Use dynamic title
        self.ax.set_xlabel("Time", color="white")
        self.ax.set_ylabel("Value", color="white")

        # Update tick labels to use white font
        self.ax.tick_params(colors="white")  # Axis ticks
        # Set the spines to be transparent
        for spine in self.ax.spines.values():
            spine.set_color((1, 1, 1, 0.5))  # RGBA: Fully transparent
        
        # Redraw the canvas
        self.canvas_widget.draw()

    def update_title(self, *args):
        """Update the chart title."""
        self.ax.set_title(self.title)
        self.canvas_widget.draw()
