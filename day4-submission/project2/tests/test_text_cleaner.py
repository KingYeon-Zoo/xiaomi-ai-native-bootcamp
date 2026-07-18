from spam_filter.text_cleaner import clean_text, extract_raw_message


def test_extract_contract_keeps_subject_and_body_but_not_headers():
    raw = (
        b"From: sender@example.com\nSubject: Special Offer\nContent-Type: text/plain; charset=utf-8\n\n"
        b"Call me at 123-456-7890 or visit https://example.com"
    )
    message = extract_raw_message(raw)
    assert "Special Offer" in message
    assert "Call me" in message
    assert "sender@example.com" not in message


def test_clean_text_covers_noise_and_empty_boundary():
    cleaned = clean_text("<b>FREE</b> at Test@Example.com! https://x.test 123-456-7890")
    assert cleaned == "free"
    assert clean_text(None) == ""
    assert clean_text("the and to") == ""


def test_html_script_content_is_not_treated_as_message_text():
    assert clean_text("<style>free</style><p>Hello</p><script>prize</script>") == "hello"

