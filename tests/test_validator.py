import pytest

from utils.validator import (
    is_valid_domain,
    is_valid_ip,
    validate_port_range,
    validate_target,
)


class TestIsValidIp:
    def test_accepts_valid_ipv4(self) -> None:
        assert is_valid_ip("192.168.1.1") is True

    def test_rejects_out_of_range_octet(self) -> None:
        assert is_valid_ip("999.1.1.1") is False

    def test_rejects_shorthand_form(self) -> None:
        # inet_aton would accept this; inet_pton correctly rejects it.
        assert is_valid_ip("192.168.1") is False

    def test_rejects_non_ip_string(self) -> None:
        assert is_valid_ip("not-an-ip") is False


class TestIsValidDomain:
    def test_accepts_simple_domain(self) -> None:
        assert is_valid_domain("example.com") is True

    def test_rejects_empty_string(self) -> None:
        assert is_valid_domain("") is False

    def test_rejects_leading_dot(self) -> None:
        assert is_valid_domain(".example.com") is False

    def test_rejects_trailing_dot(self) -> None:
        assert is_valid_domain("example.com.") is False

    def test_rejects_double_dot(self) -> None:
        assert is_valid_domain("example..com") is False

    def test_rejects_no_dot(self) -> None:
        assert is_valid_domain("localhost") is False


class TestValidateTarget:
    def test_returns_ip_unchanged(self) -> None:
        assert validate_target("10.0.0.1") == "10.0.0.1"

    def test_returns_domain_unchanged(self) -> None:
        assert validate_target("example.com") == "example.com"

    def test_raises_on_invalid_target(self) -> None:
        with pytest.raises(ValueError):
            validate_target("not..valid")


class TestValidatePortRange:
    def test_valid_range(self) -> None:
        assert validate_port_range("20", "80") == (20, 80)

    def test_rejects_non_integer(self) -> None:
        with pytest.raises(ValueError):
            validate_port_range("abc", "80")

    def test_rejects_below_minimum(self) -> None:
        with pytest.raises(ValueError):
            validate_port_range("0", "80")

    def test_rejects_above_maximum(self) -> None:
        with pytest.raises(ValueError):
            validate_port_range("20", "70000")

    def test_rejects_start_greater_than_end(self) -> None:
        with pytest.raises(ValueError):
            validate_port_range("80", "20")
