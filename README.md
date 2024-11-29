# Tor HTTP Client

`tor_http_client` is a Python package designed to make HTTP requests through the Tor network. This client routes your HTTP requests via Tor, providing enhanced privacy and anonymity for your web activities.

## Features

- **Anonymity**: Routes your HTTP/HTTPS requests through the Tor network to hide your IP address
- **Multiple HTTP Methods**: Supports GET, POST, PUT, and DELETE requests
- **Session Management**: Export and manage session data, including cookies and headers
- **Batch Processing**: Make multiple requests efficiently with retry capability
- **IP Management**: Change IP addresses on demand and manage blocked IPs
- **Retry Mechanism**: Automatic retry with configurable delays for failed requests
- **Debugging**: Comprehensive logging system with debug mode option
- **Cookie Management**: Methods to handle and clear cookies
- **Header Management**: Set and retrieve custom headers
- **Connection Verification**: Built-in methods to verify Tor connection
- **Timeout Control**: Configurable request timeouts

## Installation

To install `tor_http_client`, use pip:

```bash
pip install git+https://github.com/wendelfrota/tor-http-client.git
```

## Requirements

- **Tor**: Must be installed and configured on your system
- **Python Dependencies**: 
  - requests
- **System Requirements**: 
  - Linux system with systemctl (for Tor service management)
  - sudo privileges for Tor service operations

## Basic Usage

```python
from tor_http_client import TorHttpClient

# Initialize with debug mode
client = TorHttpClient(tor_port=9050, debug=True)

# Basic GET request
response = client.get('https://example.com')

# POST request with data
response = client.post('https://api.example.com/data', json={'key': 'value'})

# Change IP address
client.change_ip()

# Verify Tor connection
is_connected = client.verify_tor_connection()

# Check current IP
current_ip = client.show_ip()
```

## Advanced Features

### Batch Requests
```python
urls = ['https://site1.com', 'https://site2.com']
responses = client.batch_requests(urls, max_retries=3, retry_delay=5)
```

### Session Management
```python
# Export session data
client.export_session('session.json')

# Manage cookies
client.clear_cookies()
cookies = client.get_cookies()

# Set custom headers
client.set_headers({'User-Agent': 'Custom Agent'})
```

### IP Management
```python
# Check if current IP is blocked
is_blocked = client.check_ip_blocked('blocked_ips.json')

# Change IP if blocked
if is_blocked:
    client.change_ip()
```

## Available Methods

### HTTP Methods
- `get(url, **kwargs)`: Make GET request
- `post(url, data=None, json=None, **kwargs)`: Make POST request
- `put(url, data=None, json=None, **kwargs)`: Make PUT request
- `delete(url, **kwargs)`: Make DELETE request
- `batch_requests(urls: List[str], max_retries, retry_delay, method='get', **kwargs)`: Process multiple URLs

### Session Management
- `export_session(file_path: str)`: Export session data to file
- `set_timeout(timeout)`: Set request timeout
- `clear_cookies()`: Clear session cookies
- `get_cookies()`: Get current cookies
- `set_headers(headers)`: Set custom headers
- `get_headers()`: Get current headers

### Tor Management
- `change_ip()`: Change Tor exit node
- `show_ip()`: Display current IP
- `verify_tor_connection()`: Check Tor connection status
- `check_ip_blocked(blocked_ips_file: Optional[str])`: Check if current IP is blocked

## Configuration

### Debug Mode
Enable debug mode for detailed logging:
```python
client = TorHttpClient(debug=True)
```

### Custom Tor Port
Specify a custom Tor port:
```python
client = TorHttpClient(tor_port=9051)
```

## Error Handling

The client includes comprehensive error handling and logging:
- Failed requests are logged with detailed error messages
- Connection issues are handled gracefully
- Retry mechanism for failed requests
- Debug logging when enabled

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Repository

The source code for `tor_http_client` is hosted on GitHub: [tor-http-client](https://github.com/wendelfrota/tor-http-client)

## Acknowledgments

- The Tor Project team for their amazing work on privacy and anonymity
- Inspired by other privacy-focused tools and libraries
- All contributors to this project
