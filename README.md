# Tor HTTP Client

`tor_http_client` is a Python package designed to make HTTP requests through the Tor network. This client routes your HTTP requests via Tor, providing enhanced privacy and anonymity for your web activities.

## Features

- **Anonymity**: Routes your HTTP/HTTPS requests through the Tor network to hide your IP address.
- **IP Management**: Easily change your IP address by reloading Tor.
- **Debugging**: Option to display the current IP address for verification.
- **Simple Integration**: Easy to use with minimal setup.

## Installation

To install `tor_http_client`, use pip:

```bash
pip install git+https://github.com/wendelfrota/tor-http-client.git
```

## Requirements

- **Tor**: Ensure that Tor is installed and configured on your system.
- **Requests Library**: The requests library is required and will be installed automatically.

## Usage

Here is a basic example of how to use the `TorHttpClient` class:

```python
from tor_http_client import TorHttpClient

# Initialize the client (default Tor port is 9050)
client = TorHttpClient(debug=True)

# Make a GET request through Tor
response = client.get('https://google.com')
print(response.text)

# Change IP address by reloading Tor
client.change_ip()

# Display the current IP address
client.show_ip()
```

## Methods

- `__init__(tor_port=9050, debug=False)`: Initializes the client and starts Tor.
- `get(url)`: Makes an HTTP/HTTPS GET request through the Tor network.
- `change_ip()`: Reloads Tor to change the IP address.
- `show_ip()`: Displays the current IP address.
- `response`: Property that returns the most recent HTTP response.

## Troubleshooting

- **Starting Tor**: Ensure Tor is properly installed and configured on your system. The package uses `systemctl` to start and reload Tor, which requires root privileges.
- **Debugging**: If `debug` is set to `True`, the current IP address will be displayed. This helps in verifying that the requests are routed through Tor.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Repository

The source code for `tor_http_client` is hosted on GitHub: [tor-http-client](https://github.com/wendelfrota/tor-http-client)

## Acknowledgments

- Thanks to the Tor Project for their work on the Tor network.
- Inspired by other privacy-focused tools and libraries.
