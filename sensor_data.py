class SensorData:
    def __init__(self, sensor_id, temperature, timestamp):
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.timestamp = timestamp


class SensorLogger:
    def __init__(self):
        self._sensor_data = {}
        self.enable_logging = False

    def log_data(self, sensor_data: SensorData):
        if not self.enable_logging:
            return
        if sensor_data.sensor_id in self._sensor_data:
            self._sensor_data[sensor_data.sensor_id].append(sensor_data)
        else:
            self._sensor_data[sensor_data.sensor_id] = [sensor_data]

    def get_data(self, sensor_id):
        return self._sensor_data.get(sensor_id)
