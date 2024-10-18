import requests
import subprocess
from contextlib import contextmanager
from typing import Optional


class TorHttpClient:
    def __init__(self, tor_port: int = 9050, debug: bool = False) -> None:
        self.__session = requests.Session()
        self.__response: Optional[requests.Response] = None
        self.__tor_port: int = tor_port
        self.__debug: bool = debug
        self.__start_tor()

    @property
    def response(self) -> Optional[requests.Response]:
        return self.__response

    def __start_tor(self):
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)

            if self.__debug:
                self.show_ip()
        except subprocess.CalledProcessError as e:
            print(f'Failed to start Tor: {e}')

    @contextmanager
    def __tor_session(self):
        self.__session.proxies = {
            'http': f'socks5://127.0.0.1:{self.__tor_port}',
            'https': f'socks5://127.0.0.1:{self.__tor_port}'
        }
        try:
            yield self.__session
        finally:
            self.__session.close()

    def __request(self, method, url, **kwargs):
        with self.__tor_session() as session:
            try:
                self.__response = session.request(method, url, **kwargs)
                self.__response.raise_for_status()
                return self.__response
            except requests.RequestException as e:
                self.__response = None
                return None

    def get(self, url, **kwargs) -> Optional[requests.Response]:
        return self.__request('get', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> Optional[requests.Response]:
        return self.__request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, json=None, **kwargs) -> Optional[requests.Response]:
        return self.__request('put', url, data=data, json=json, **kwargs)

    def delete(self, url, **kwargs) -> Optional[requests.Response]:
        return self.__request('delete', url, **kwargs)

    def change_ip(self):
        self.__reload_tor()

        if self.__debug:
            self.show_ip()

    def show_ip(self):
        try:
            ip = self.get('https://httpbin.org/ip').text
            print(f'[+] IP : {ip}')
        except AttributeError:
            print('[!] Failed to retrieve the IP address.')

    def __reload_tor(self):
        try:
            subprocess.run(['sudo', 'systemctl', 'reload', 'tor'], check=True)
        except subprocess.CalledProcessError as e:
            print(f'Failed to reload Tor: {e}')
