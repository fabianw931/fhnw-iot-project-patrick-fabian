import requests
from time import time, sleep

class ThingSpeakService:

    def __init__(self, channel, api_key):
        self.url = 'https://api.thingspeak.com/channels/'
        self.channel = channel
        self.api_key = api_key
        self.co2_field = 'field1'
        self.temp_field = 'field2'
        self.hum_field = 'field3'
        self.read_delay = 10
        self.last_read_time = 0
        self.last_reading = ""
        

    def get_readings_json(self, nr_readings):
        current_time = time()
        if current_time - self.last_read_time > self.read_delay:
            try:
                self.last_read_time = current_time
                req = self.url + str(self.channel) + '/feeds.json?api_key=' + self.api_key + '&results=' + str(nr_readings)
                response = requests.get(req)
                if response.status_code == 200:
                    self.last_reading = response.json()
                    return response.json()
                else:
                    return self.last_reading
            except:
                return self.last_reading
        else:
            return self.last_reading

    def get_field(self, field_name, num_readings):
        json = self.get_readings_json(num_readings)
        feeds = json.get('feeds')
        if num_readings == 1:
            return feeds[0].get(field_name)
        else:
            readings = []
            for i in range(num_readings):
                readings.append(feeds[i].get(field_name))
            return readings

    def get_co2(self, nr=1):
        value = self.get_field(self.co2_field, nr)
        return 0 if value is None else int(value)

    def get_temp(self, nr=1):
        value = self.get_field(self.temp_field, nr)
        return 0 if value is None else float(value)

    def get_hum(self, nr=1):
        value = self.get_field(self.hum_field, nr)
        return 0 if value is None else float(value)