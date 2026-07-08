import socket
from unittest.mock import patch

import pytest

from scanner.resolver import resolve_target


class TestResolveTarget:
    def test_ip_returned_unchanged(self) -> None:
        assert resolve_target("8.8.8.8") == "8.8.8.8"

    def test_domain_resolved_via_dns(self) -> None:
        with patch(
            "scanner.resolver.socket.gethostbyname", return_value="93.184.216.34"
        ) as mock_resolve:
            assert resolve_target("example.com") == "93.184.216.34"
            mock_resolve.assert_called_once_with("example.com")

    def test_unresolvable_domain_raises_value_error(self) -> None:
        with patch("scanner.resolver.socket.gethostbyname", side_effect=socket.gaierror):
            with pytest.raises(ValueError):
                resolve_target("does-not-resolve.invalid")

    def test_invalid_target_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            resolve_target("not a target")
