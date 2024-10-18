import subprocess
from contextlib import contextmanager

import requests
from typing import Optional, Dict, Any


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

    def get(self, url: str) -> Optional[requests.Response]:
        try:
            self.__response = requests.get(
                url=url,
                proxies={
                    'http': f'socks5://127.0.0.1:{self.__tor_port}',
                    'https': f'socks5://127.0.0.1:{self.__tor_port}'
                }
            )
            self.__response.raise_for_status()
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
            self.__response = None
        return self.__response

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        try:
            self.__response = requests.post(
                url=url,
                data=data,
                json=json,
                proxies={
                    'http': f'socks5://127.0.0.1:{self.__tor_port}',
                    'https': f'socks5://127.0.0.1:{self.__tor_port}'
                }
            )
            self.__response.raise_for_status()
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
            self.__response = None
        return self.__response

    def put(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        try:
            self.__response = requests.put(
                url=url,
                data=data,
                json=json,
                proxies={
                    'http': f'socks5://127.0.0.1:{self.__tor_port}',
                    'https': f'socks5://127.0.0.1:{self.__tor_port}'
                }
            )
            self.__response.raise_for_status()
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
            self.__response = None
        return self.__response

    def delete(self, url: str) -> Optional[requests.Response]:
        try:
            self.__response = requests.delete(
                url=url,
                proxies={
                    'http': f'socks5://127.0.0.1:{self.__tor_port}',
                    'https': f'socks5://127.0.0.1:{self.__tor_port}'
                }
            )
            self.__response.raise_for_status()
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
            self.__response = None
        return self.__response

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
