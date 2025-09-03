import ipaddress
import re

from data.pipelines.pipeline import mask_email, mask_phone, anonymize_ip, tokenize_last4, build_field_constraints


def test_mask_email_normalizes_and_hashes():
    a = mask_email(" Alice@example.com ")
    b = mask_email("alice@EXAMPLE.com")
    assert a == b
    assert a.endswith("@redacted.local")
    assert a.startswith("u_")


def test_mask_phone_masks_digits():
    assert mask_phone("+1 (415) 555-0101").startswith("+**")
    assert mask_phone("+1 (415) 555-0101").endswith("01")
    assert mask_phone("") == ""


def test_anonymize_ip_ipv4_zeroes_octets():
    masked = anonymize_ip("192.168.2.55")
    assert masked == "192.168.0.0"


def test_anonymize_ip_ipv6_returns_network():
    masked = anonymize_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    # ensure valid IPv6 and /64 network base
    ipaddress.IPv6Address(masked)
    assert masked.endswith("::")


def test_anonymize_ip_invalid_returns_default():
    assert anonymize_ip("not_an_ip") == "0.0.0.0"


def test_tokenize_last4_stable_prefix():
    tok = tokenize_last4("4242")
    assert tok.startswith("tok_")
    assert re.fullmatch(r"tok_[0-9a-f]{8}", tok)


def test_build_field_constraints_merges_options():
    spec = {"constraints": ["unique", {"enum": ["A", "B"]}, {"min": 0}]}
    c = build_field_constraints(spec)
    assert c["unique"] is True
    assert c["enum"] == ["A", "B"]
    assert c["min"] == 0