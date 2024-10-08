import subprocess
import requests


class TorHttpClient:
    def __init__(self, tor_port=9050, debug=False):
        self.__response = None
        self.__tor_port = tor_port
        self.__debug = debug
        self.__start_tor()

    @property
    def response(self):
        return self.__response

    def __start_tor(self):
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)

            if self.__debug:
                self.show_ip()
        except subprocess.CalledProcessError as e:
            print(f'Failed to start Tor: {e}')

    def get(self, url):
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

    def post(self, url, data=None, json=None):
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

    def put(self, url, data=None, json=None):
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

    def delete(self, url):
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
