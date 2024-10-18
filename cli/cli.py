import json
import argparse
import requests
from thc.tor_http_client import TorHttpClient


def main():
    parser = argparse.ArgumentParser(description='A simple HTTP client over Tor.')
    parser.add_argument('url', help='URL to request')
    parser.add_argument('-m', '--method', choices=['GET', 'POST', 'PUT', 'DELETE'], default='GET', help='HTTP method to use')
    parser.add_argument('-d', '--data', help='Data to send with the request')
    parser.add_argument('-j', '--json', help='JSON data to send with the request')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    client = TorHttpClient(debug=args.debug)

    match args.method:
        case 'GET':
            response = client.get(args.url)
        case 'POST':
            response = client.post(args.url, args.data, args.json)
        case 'PUT':
            response = client.put(args.url, args.data, args.json)
        case 'DELETE':
            response = client.delete(args.url)
        case _:
            response = None

    if isinstance(response, requests.Response):
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except ValueError:
            print(response.text)


if __name__ == '__main__':
    main()
