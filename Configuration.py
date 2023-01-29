import configparser


class Configuration:
    def __init__(self, config_file_name):
        self.config = configparser.ConfigParser()
        self.config.read(config_file_name)

        self.default_section = self.config['DEFAULT']

    def get_room_size(self):
        return int(self.default_section['room_size'])

    def get_port(self):
        return int(self.default_section['port'])

    def get_hostname(self):
        return self.default_section['hostname']

    def get_server_name(self):
        return self.default_section['server_name']
