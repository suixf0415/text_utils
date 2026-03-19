"""Tests for extraction utilities."""

from text_utils import extractor


class TestExtractEmails:
    """Tests for extract_emails function."""

    def test_extract_basic(self):
        text = "Contact: test@example.com or info@test.org"
        result = extractor.extract_emails(text)
        assert "test@example.com" in result
        assert "info@test.org" in result

    def test_extract_deduplicate(self):
        text = "a@test.com and a@test.com"
        result = extractor.extract_emails(text)
        assert len(result) == 1

    def test_extract_no_match(self):
        text = "No email here"
        result = extractor.extract_emails(text)
        assert result == []


class TestExtractPhones:
    """Tests for extract_phones function."""

    def test_extract_cn_mobile(self):
        text = "Phone: 13812345678 or 19987654321"
        result = extractor.extract_phones(text, region="cn")
        assert "13812345678" in result or "19987654321" in result

    def test_extract_cn_with_prefix(self):
        text = "+8613912345678"
        result = extractor.extract_phones(text, region="cn")
        assert "13912345678" in result or "+8613912345678" in result

    def test_extract_us(self):
        text = "Call (555) 123-4567"
        result = extractor.extract_phones(text, region="us")
        assert len(result) >= 1

    def test_extract_cn_landline_with_dash(self):
        text = "Call: 010-12345678 or 021-87654321"
        result = extractor.extract_phones(text, region="cn")
        assert "010-12345678" in result
        assert "021-87654321" in result

    def test_extract_cn_landline_with_space(self):
        text = "Call: 021 87654321 or 0755 12345678"
        result = extractor.extract_phones(text, region="cn")
        assert "021 87654321" in result
        assert "0755 12345678" in result

    def test_extract_cn_mobile_with_dash(self):
        text = "Call: 138-1234-5678 or 199-1234-5678"
        result = extractor.extract_phones(text, region="cn")
        assert "138-1234-5678" in result
        assert "199-1234-5678" in result

    def test_extract_cn_mobile_with_space(self):
        text = "Call: 138 1234 5678 or 199 1234 5678"
        result = extractor.extract_phones(text, region="cn")
        assert "138 1234 5678" in result
        assert "199 1234 5678" in result

    def test_extract_cn_international_with_plus(self):
        text = "Call: +86 138 1234 5678 or +86-138-1234-5678"
        result = extractor.extract_phones(text, region="cn")
        assert "+86 138 1234 5678" in result
        assert "+86-138-1234-5678" in result

    def test_extract_cn_international_landline(self):
        text = "Call: +86 010 12345678 or +86-021-87654321"
        result = extractor.extract_phones(text, region="cn")
        assert "+86 010 12345678" in result
        assert "+86-021-87654321" in result

    def test_extract_cn_landline_no_separator(self):
        text = "02187654321 or 075512345678"
        result = extractor.extract_phones(text, region="cn")
        assert "02187654321" in result
        assert "075512345678" in result

    def test_landline_area_code_must_start_with_zero(self):
        text = "12345678901"
        result = extractor.extract_phones(text, region="cn")
        assert result == []

    def test_landline_invalid_area_code_rejected(self):
        text = "12-12345678 or 13-87654321"
        result = extractor.extract_phones(text, region="cn")
        assert result == []

    def test_landline_valid_3digit_area_code(self):
        text = "01012345678 or 02087654321"
        result = extractor.extract_phones(text, region="cn")
        assert "01012345678" in result
        assert "02087654321" in result

    def test_landline_valid_4digit_area_code(self):
        text = "07911234567 or 075512345678"
        result = extractor.extract_phones(text, region="cn")
        assert "07911234567" in result
        assert "075512345678" in result

    def test_extract_cn_400_service(self):
        text = "Hotline: 400-123-4567 or 40012345678"
        result = extractor.extract_phones(text, region="cn")
        assert "400-123-4567" in result
        assert "40012345678" in result

    def test_extract_cn_800_service(self):
        text = "Hotline: 800-123-4567 or 800-1234567"
        result = extractor.extract_phones(text, region="cn")
        assert "800-123-4567" in result
        assert "800-1234567" in result

    def test_extract_cn_400_with_space(self):
        text = "Hotline: 400 123 4567"
        result = extractor.extract_phones(text, region="cn")
        assert "400 123 4567" in result

    def test_extract_cn_800_international(self):
        text = "Call: +86 400 123 4567 or +86-800-123-4567"
        result = extractor.extract_phones(text, region="cn")
        assert "+86 400 123 4567" in result
        assert "+86-800-123-4567" in result


class TestExtractUrls:
    """Tests for extract_urls function."""

    def test_extract_basic(self):
        text = "Visit https://example.com or http://test.org"
        result = extractor.extract_urls(text)
        assert "https://example.com" in result
        assert "http://test.org" in result

    def test_extract_no_match(self):
        text = "No URL here"
        result = extractor.extract_urls(text)
        assert result == []


class TestExtractIPv4:
    """Tests for extract_ipv4 function."""

    def test_extract_basic(self):
        text = "IP: 192.168.1.1 or 10.0.0.1"
        result = extractor.extract_ipv4(text)
        assert "192.168.1.1" in result
        assert "10.0.0.1" in result

    def test_extract_invalid(self):
        text = "Not an IP: 999.999.999.999"
        result = extractor.extract_ipv4(text)
        assert result == []


class TestExtractIPv6:
    """Tests for extract_ipv6 function."""

    def test_extract_basic(self):
        text = "IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        result = extractor.extract_ipv6(text)
        assert len(result) >= 1

    def test_extract_compressed(self):
        text = "Server: 2001:db8::1"
        result = extractor.extract_ipv6(text)
        assert "2001:db8::1" in result

    def test_extract_loopback(self):
        text = "localhost is ::1"
        result = extractor.extract_ipv6(text)
        assert "::1" in result

    def test_extract_unspecified(self):
        text = "default route is ::"
        result = extractor.extract_ipv6(text)
        assert "::" in result

    def test_extract_ipv4_mapped(self):
        text = "mapped: ::ffff:192.0.2.1"
        result = extractor.extract_ipv6(text)
        assert "::ffff:192.0.2.1" in result

    def test_extract_link_local(self):
        text = "fe80::1"
        result = extractor.extract_ipv6(text)
        assert "fe80::1" in result

    def test_extract_trailing_colons(self):
        text = "doc: 2001:db8::"
        result = extractor.extract_ipv6(text)
        assert "2001:db8::" in result


class TestExtractIDCards:
    """Tests for extract_id_cards function."""

    def test_extract_valid(self):
        text = "ID: 110101199001011234"
        result = extractor.extract_id_cards(text)
        assert "110101199001011234" in result

    def test_extract_invalid(self):
        text = "Not an ID: 000000000000000000"
        result = extractor.extract_id_cards(text)
        assert result == []


class TestExtractHashtags:
    """Tests for extract_hashtags function."""

    def test_extract_basic(self):
        text = "Tags: #python #programming"
        result = extractor.extract_hashtags(text)
        assert "#python" in result
        assert "#programming" in result


class TestExtractMentions:
    """Tests for extract_mentions function."""

    def test_extract_basic(self):
        text = "Mention: @user1 and @user2"
        result = extractor.extract_mentions(text)
        assert "@user1" in result
        assert "@user2" in result


class TestExtractDates:
    """Tests for extract_dates function."""

    def test_extract_iso(self):
        text = "Date: 2024-01-15"
        result = extractor.extract_dates(text, format="iso")
        assert "2024-01-15" in result

    def test_extract_cn(self):
        text = "Date: 2024年1月15日"
        result = extractor.extract_dates(text, format="cn")
        assert "2024年1月15日" in result


class TestExtractNumbers:
    """Tests for extract_numbers function."""

    def test_extract_integers(self):
        text = "Numbers: 123 and 456"
        result = extractor.extract_numbers(text, decimal=False)
        assert "123" in result
        assert "456" in result

    def test_extract_decimals(self):
        text = "Decimals: 1.5 and 2.3"
        result = extractor.extract_numbers(text, decimal=True)
        assert "1.5" in result
        assert "2.3" in result


class TestExtractWords:
    """Tests for extract_words function."""

    def test_extract_basic(self):
        text = "Hello world from Python"
        result = extractor.extract_words(text)
        assert "Hello" in result
        assert "world" in result
        assert "Python" in result

    def test_extract_min_length(self):
        text = "a ab abc"
        result = extractor.extract_words(text, min_length=2)
        assert "ab" in result
        assert "abc" in result
        assert "a" not in result


class TestExtractHexColors:
    """Tests for extract_hex_colors function."""

    def test_extract_3_digit(self):
        text = "Color: #fff"
        result = extractor.extract_hex_colors(text)
        assert "#fff" in result

    def test_extract_6_digit(self):
        text = "Color: #ff0000"
        result = extractor.extract_hex_colors(text)
        assert "#ff0000" in result


class TestLuhnCheck:
    """Tests for luhn_check function."""

    def test_valid_card(self):
        assert extractor.luhn_check("4532015112830366") is True

    def test_invalid_card(self):
        assert extractor.luhn_check("4532015112830367") is False

    def test_empty_string(self):
        assert extractor.luhn_check("") is False

    def test_non_digit(self):
        assert extractor.luhn_check("abc") is False

    def test_13_digit_card(self):
        assert extractor.luhn_check("4000000000006") is True

    def test_14_digit_card(self):
        assert extractor.luhn_check("30000000000004") is True

    def test_15_digit_card(self):
        assert extractor.luhn_check("371449635398431") is True

    def test_18_digit_card(self):
        assert extractor.luhn_check("601111111111111114") is True

    def test_single_digit(self):
        assert extractor.luhn_check("0") is True

    def test_two_digits(self):
        assert extractor.luhn_check("55") is False

    def test_mixed_valid_invalid(self):
        assert extractor.luhn_check("4532015112830367") is False


class TestExtractBankCards:
    """Tests for extract_bank_cards function."""

    def test_extract_valid_card(self):
        text = "Card: 4532015112830366"
        result = extractor.extract_bank_cards(text)
        assert "4532015112830366" in result

    def test_extract_invalid_card_filtered(self):
        text = "Card: 4532015112830367"
        result = extractor.extract_bank_cards(text, validate=True)
        assert result == []

    def test_extract_invalid_card_included_without_validation(self):
        text = "Card: 4532015112830367"
        result = extractor.extract_bank_cards(text, validate=False)
        assert "4532015112830367" in result

    def test_extract_with_spaces(self):
        text = "Card: 4532 0151 1283 0366"
        result = extractor.extract_bank_cards(text)
        assert "4532015112830366" in result

    def test_extract_with_dashes(self):
        text = "Card: 4532-0151-1283-0366"
        result = extractor.extract_bank_cards(text)
        assert "4532015112830366" in result

    def test_extract_deduplicate(self):
        text = "Card: 4532015112830366 and 4532015112830366"
        result = extractor.extract_bank_cards(text)
        assert len(result) == 1

    def test_extract_16_digit(self):
        text = "Bank card number: 5425233430109903"
        result = extractor.extract_bank_cards(text)
        assert "5425233430109903" in result

    def test_extract_19_digit(self):
        text = "Card: 6011111111111117000"
        result = extractor.extract_bank_cards(text)
        assert "6011111111111117000" in result

    def test_extract_13_digit(self):
        text = "Card: 4000000000006"
        result = extractor.extract_bank_cards(text)
        assert "4000000000006" in result

    def test_extract_14_digit(self):
        text = "Card: 30000000000004"
        result = extractor.extract_bank_cards(text)
        assert "30000000000004" in result

    def test_extract_15_digit(self):
        text = "Card: 371449635398431"
        result = extractor.extract_bank_cards(text)
        assert "371449635398431" in result

    def test_extract_17_digit(self):
        text = "Card: 60111111111111113"
        result = extractor.extract_bank_cards(text)
        assert "60111111111111113" in result

    def test_extract_18_digit(self):
        text = "Card: 601111111111111114"
        result = extractor.extract_bank_cards(text)
        assert "601111111111111114" in result

    def test_extract_invalid_length_12_filtered(self):
        text = "Card: 123456789012"
        result = extractor.extract_bank_cards(text)
        assert result == []

    def test_extract_invalid_length_20_filtered(self):
        text = "Card: 12345678901234567890"
        result = extractor.extract_bank_cards(text)
        assert result == []

    def test_extract_mixed_valid_invalid(self):
        text = "Valid: 4532015112830366 Invalid: 4532015112830367"
        result = extractor.extract_bank_cards(text)
        assert len(result) == 1
        assert "4532015112830366" in result

    def test_extract_no_cards(self):
        text = "No card numbers here: 1234"
        result = extractor.extract_bank_cards(text)
        assert result == []
