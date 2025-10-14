"""
Compatibility shim: top-level `email_service.py` proxies to
`shop.email_service`.
"""

from shop.email_service import (
    BytesIO,
    Decimal,
    EmailMultiAlternatives,
    Paragraph,
    ParagraphStyle,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    colors,
    generate_invoice_pdf,
    getSampleStyleSheet,
    inch,
    letter,
    render_to_string,
    send_order_confirmation_email,
    send_order_status_update_email,
    strip_tags,
)

__all__ = [
    "BytesIO",
    "Decimal",
    "EmailMultiAlternatives",
    "Paragraph",
    "ParagraphStyle",
    "SimpleDocTemplate",
    "Spacer",
    "Table",
    "TableStyle",
    "colors",
    "generate_invoice_pdf",
    "getSampleStyleSheet",
    "inch",
    "letter",
    "render_to_string",
    "send_order_confirmation_email",
    "send_order_status_update_email",
    "strip_tags",
]
