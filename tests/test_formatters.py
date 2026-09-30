from services.document_formatter import (
    format_docx,
    format_pdf,
    format_txt
)


def test_txt_export():

    data = format_txt(
        "HELLO\nWorld"
    )

    assert isinstance(
        data,
        bytes
    )

    assert b"HELLO" in data


def test_docx_export():

    data = format_docx(
        "PARTIES\n\nAlice and Bob",
        "Agreement"
    )

    assert data[:2] == b"PK"


def test_pdf_export():

    data = format_pdf(
        "PARTIES\n\nAlice and Bob",
        "Agreement"
    )

    assert data.startswith(
        b"%PDF"
    )