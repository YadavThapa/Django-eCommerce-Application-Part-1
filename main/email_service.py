"""
Compatibility shim: top-level `email_service.py` proxies to
`shop.email_service`.
"""

try:
    # Prefer the canonical location so static analyzers (pylint, IDEs)
    # can resolve the module. At runtime the top-level `shop` package
    # is a small shim that aliases `main.shop` to `shop`, but linters
    # may not evaluate that dynamic assignment.
    from main.shop.email_service import (
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
except (ImportError, ModuleNotFoundError):  # pragma: no cover - compatibility fallback
    # Fallback to importing from the top-level `shop` package. This
    # keeps backwards compatible import paths working in case the
    # shim isn't active in some environments.
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
