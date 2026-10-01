import socket
import threading

import pytest

from api_client.practice_api import make_server


@pytest.fixture(scope="module")
def base_url():
    """Run the practice API on a free port for the duration of a test module."""
    server = make_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    yield f"http://{host}:{port}"
    server.shutdown()
    server.server_close()


@pytest.fixture
def closed_port_url():
    """A URL on which nothing is listening, so connecting is refused."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    return f"http://127.0.0.1:{port}"
