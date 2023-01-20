import time
from sensor_data import SensorLogger
import numpy as np

from nicegui import ui
from matplotlib import pyplot as plt
from datetime import datetime
from threading import Thread


class WebUI:
    def __init__(self, sensor_logger: SensorLogger):
        self._sensor_logger = sensor_logger
        self.__draw_ui__()

    def run(self):
        t = Thread(target=self._label_updater)
        t.start()
        ui.run(reload=False)

    def _label_updater(self):
        while True:
            if not self._sensor_logger.enable_logging:
                self._label1.set_text("No Active Measurements")
            else:
                sd = self._sensor_logger.get_data(sensor_id="pico_fb")
                if sd is not None:
                    last_data = sd[-1]
                    self._label1.set_text("Sensor ID: " + last_data.sensor_id + " Temperature: " +
                                          last_data.temperature + " " +
                                          datetime.fromtimestamp(last_data.timestamp).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    self._label1.set_text("Sensor Pico_fb")
            time.sleep(1.0)

    def _start_measurement(self):
        self._sensor_logger.enable_logging = True
        ui.notify("Starting Measuring")

    def _stop_measurement(self):
        self._sensor_logger.enable_logging = False
        ui.notify("Stop Measuring")

    def __draw_ui__(self):
        with ui.row():
            self._label1 = ui.label("1")
            label2 = ui.label("2")
            label3 = ui.label("3")
            label4 = ui.label("4")

        with ui.row():
            with ui.plot(figsize=(5, 3)):
                x = np.linspace(0.0, 5.0)
                y1 = np.linspace(0.0, 6.1)
                y2 = np.linspace(0.0, 5)
                y3 = np.linspace(0.0, 54)
                y4 = np.linspace(0.0, 12)
                plt.plot(x, y1, '-', x, y2, '-', x, y3, '-', x, y4, '-')

        ui.label("Auto Mode")
        with ui.row():
            slider = ui.slider(min=0, max=75, step=1, value=20)
            ui.linear_progress().bind_value_from(slider, 'value')
            ui.button('Auto Mode Start', on_click=lambda: self._start_measurement())
            ui.button('Stop Measurements', on_click=lambda: self._stop_measurement())

        ui.label("Manual Mode")
        with ui.row():
            ui.button('Heaters On', on_click=lambda: ui.notify(f'You clicked me!'))
            ui.button('Ventilators On', on_click=lambda: ui.notify(f'You clicked me!'))
        with ui.row():
            ui.button('Ventilators Off', on_click=lambda: ui.notify(f'You clicked me!'))
            ui.button('Heaters Off', on_click=lambda: ui.notify(f'You clicked me!'))