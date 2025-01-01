import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
import paho.mqtt.client as mqtt


class Gauge(BoxLayout):
    current_value = NumericProperty(50)  # Default value for the gauge
    min_value = NumericProperty(0)       # Minimum range for the gauge
    max_value = NumericProperty(100)     # Maximum range for the gauge
    title = StringProperty("Gauge Chart")  # Title of the gauge
    mqtt_server = StringProperty("192.168.1.152")  # MQTT broker address
    mqtt_topic = StringProperty("home/loft")       # MQTT topic to subscribe to

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        # Initialize the Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(6, 3), subplot_kw={'projection': 'polar'})
        self.ax.set_theta_offset(np.pi / 2)  # Rotate to start at the top
        self.ax.set_theta_direction(-1)     # Make clockwise

        # Add the Matplotlib canvas to the Kivy widget
        self.canvas_widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(self.canvas_widget)

        # Connect to the MQTT broker
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.mqtt_server, 1883)  # Port 1883 for MQTT
        self.client.loop_start()

        # Draw the initial gauge
        self.update_gauge()

    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to the MQTT broker."""
        if rc == 0:
            print(f"Connected to MQTT broker at {self.mqtt_server}")
            client.subscribe(self.mqtt_topic)
        else:
            print("Failed to connect to MQTT broker")

    def on_message(self, client, userdata, msg):
        """Callback for receiving messages from MQTT."""
        try:
            value = float(msg.payload.decode("utf-8"))
            print(f"Received value: {value}")

            # Update the gauge value on the main Kivy thread
            Clock.schedule_once(lambda dt: self.set_value(value))
        except ValueError:
            print("Invalid payload received, expected a float")

    def set_value(self, value):
        """Set the gauge value and redraw."""
        self.current_value = value
        self.update_gauge()

    def update_gauge(self):
        """Update the gauge chart with the current value."""
        self.ax.clear()  # Clear the current plot

        # Normalize the value to range [0, 1]
        normalized_value = (self.current_value - self.min_value) / (self.max_value - self.min_value)

        # Draw gauge sections
        categories = ['Low', 'Medium', 'High']
        colors = ['#99ff99', '#ffcc66', '#ff9999']
        theta = np.linspace(0, np.pi, len(categories) + 1)
        for i in range(len(categories)):
            self.ax.bar((theta[i] + theta[i + 1]) / 2, 1, width=(theta[i + 1] - theta[i]),
                        color=colors[i], edgecolor='white', linewidth=2)

        # Draw the needle
        needle_angle = normalized_value * np.pi
        self.ax.annotate('', xy=(needle_angle, 0.9), xytext=(0, 0),
                         arrowprops=dict(facecolor='black', width=2, headwidth=8))

        # Add title
        self.ax.set_title(self.title, va='bottom', fontsize=14)

        # Remove labels
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Redraw the canvas
        self.canvas_widget.draw()
