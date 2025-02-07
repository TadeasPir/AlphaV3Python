import os
import yaml


class Config:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file {self.config_path} not found.")
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    @property
    def ip(self):
        return self._config['bank']['ip']
    @property
    def client_timeout(self):
        return self._config['bank']['timeout']

    @property
    def host(self):
        return self._config['db']['host']

    @property
    def user(self):
        return self._config['db']['user']

    @property
    def password(self):
        return self._config['db']['password']

    @property
    def database(self):
        return self._config['db']['database']

    @property
    def port(self):
        return int(self._config['bank']['port'])


    @property
    def logging_level(self):
        return self._config['logging']['level']

    @property
    def logging_file(self):
        return self._config['logging']['file']