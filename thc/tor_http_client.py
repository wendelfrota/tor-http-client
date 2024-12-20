import json
import time
import logging
import requests
import subprocess
from contextlib import contextmanager
from typing import Optional, Dict, List


class TorHttpClient:
    def __init__(self, tor_port: int = 9050, debug: bool = False) -> None:
        self.__session = requests.Session()
        self.__response: Optional[requests.Response] = None
        self.__tor_port: int = tor_port
        self.__debug: bool = debug
        self.__blocked_ips: List[str] = []
        self.__configure_logging()
        self.__start_tor()

    def __configure_logging(self):
        logging.basicConfig(
            level=logging.DEBUG if self.__debug else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def __start_tor(self):
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)
            self.logger.info('Tor service started successfully')
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Failed to start Tor: {e}')

    @property
    def response(self) -> Optional[requests.Response]:
        return self.__response

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

    def __reload_tor(self):
        try:
            subprocess.run(['sudo', 'systemctl', 'reload', 'tor'], check=True)
            self.logger.info('Tor service reloaded successfully')
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Failed to reload Tor: {e}')

    def __request(self, method, url, **kwargs):
        with self.__tor_session() as session:
            try:
                self.__response = session.request(method, url, **kwargs)
                self.__response.raise_for_status()
                self.logger.debug(f'{method.upper()} request to {url} successful')
                return self.__response
            except requests.RequestException as e:
                self.logger.error(f'An error occurred during {method.upper()} request to {url}: {e}')
                self.__response = None
                return None

    def __request_with_retry(self, method, url, max_retries, retry_delay, **kwargs) -> Optional[requests.Response]:
        for attempt in range(max_retries):
            try:
                response = self.__request(method, url, **kwargs)
                if response:
                    return response
            except requests.Timeout:
                self.logger.warning(f'Request timeout (attempt {attempt + 1}/{max_retries})')
            except Exception as e:
                self.logger.error(f'Request failed (attempt {attempt + 1}/{max_retries}): {e}')

            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                self.change_ip()
        return None

    def batch_requests(self, urls: List[str], max_retries, retry_delay, method: str = 'get', **kwargs) -> List[Optional[requests.Response]]:
        results = []
        for url in urls:
            try:
                response = self.__request_with_retry(method, url, max_retries, retry_delay, **kwargs)
                results.append(response)
            except Exception as e:
                self.logger.error(f'Batch request failed for {url}: {e}')
                results.append(None)
        return results

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
        response = self.get('https://httpbin.org/ip')
        if response:
            ip = response.json().get('origin')
            self.logger.info(f'Current IP: {ip}')
            return ip
        else:
            self.logger.warning('Failed to retrieve the IP address')
            return None

    def verify_tor_connection(self) -> bool:
        try:
            response = self.get('https://check.torproject.org')
            return 'Congratulations' in response.text if response else False
        except Exception as e:
            self.logger.error(f'Failed to verify Tor connection: {e}')
            return False

    def export_session(self, file_path: str) -> bool:
        try:
            session_data = {
                'cookies': dict(self.__session.cookies),
                'headers': dict(self.__session.headers),
                'proxies': self.__session.proxies
            }
            with open(file_path, 'w') as f:
                json.dump(session_data, f, indent=4)
            self.logger.info(f'Session exported to {file_path}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to export session: {e}')
            return False

    def check_ip_blocked(self, blocked_ips_file: Optional[str] = None) -> bool:
        current_ip = self.show_ip()
        if not current_ip:
            return False

        if blocked_ips_file:
            try:
                with open(blocked_ips_file, 'r') as f:
                    self.__blocked_ips = json.load(f)
                self.logger.info(f'Loaded {len(self.__blocked_ips)} blocked IPs from file')
            except Exception as e:
                self.logger.error(f'Failed to load blocked IPs from file: {e}')
                return False

        is_blocked = current_ip in self.__blocked_ips
        if is_blocked:
            self.logger.warning(f'Current IP {current_ip} is blocked')
        else:
            self.logger.debug(f'Current IP {current_ip} is not blocked')

        return is_blocked

    def set_timeout(self, timeout):
        self.__session.timeout = timeout

    def clear_cookies(self):
        self.__session.cookies.clear()
        self.logger.info('Session cookies cleared')

    def get_cookies(self) -> Dict[str, str]:
        return dict(self.__session.cookies)

    def set_headers(self, headers):
        self.__session.headers.update(headers)
        self.logger.info('Session headers updated')

    def get_headers(self) -> Dict[str, str]:
        return dict(self.__session.headers)
