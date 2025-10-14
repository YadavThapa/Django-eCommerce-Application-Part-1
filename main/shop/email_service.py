"""
Email service for order confirmations and invoice generation.
"""

import logging
from decimal import Decimal
from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.lib import colors  # type: ignore[import]
from reportlab.lib.pagesizes import letter  # type: ignore[import]
from reportlab.lib.styles import ParagraphStyle  # type: ignore[import]
from reportlab.lib.styles import getSampleStyleSheet  # type: ignore[import]
from reportlab.lib.units import inch  # type: ignore[import]
from reportlab.platypus import (  # type: ignore[import]
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)


def generate_invoice_pdf(order):
    """Generate PDF invoice for an order."""
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Container for the 'Flowable' objects
    elements = []

    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor("#2c3e50"),
    )

    # Add company header
    elements.append(Paragraph("Himalayan eCommerce", title_style))
    elements.append(Paragraph("Invoice", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    # Order information
    # Safely resolve customer display name and email for registered or guest
    buyer = getattr(order, "buyer", None)
    if buyer:
        customer_name = buyer.get_full_name() or getattr(buyer, "username", "")
        customer_email = getattr(buyer, "email", "")
    else:
        customer_name = order.guest_name or "Guest"
        customer_email = order.guest_email or ""

    order_info = [
        ["Order ID:", order.order_id],
        ["Date:", order.created_at.strftime("%B %d, %Y")],
        ["Customer:", customer_name],
        ["Email:", customer_email],
        ["Status:", order.get_status_display()],
    ]

    order_table = Table(order_info, colWidths=[2 * inch, 4 * inch])
    order_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    elements.append(order_table)
    elements.append(Spacer(1, 20))

    # Shipping address
    elements.append(Paragraph("Shipping Address:", styles["Heading3"]))
    elements.append(Paragraph(order.shipping_address, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Order items
    elements.append(Paragraph("Order Items:", styles["Heading3"]))

    # Create items table
    items_data = [["Product", "Quantity", "Unit Price", "Total"]]

    subtotal = Decimal("0.00")
    for item in order.items.all():
        item_total = item.price * item.quantity
        subtotal += item_total
        items_data.append(
            [
                item.product.name,
                str(item.quantity),
                f"${item.price:.2f}",
                f"${item_total:.2f}",
            ]
        )

    items_table = Table(
        items_data, colWidths=[3 * inch, 1 * inch, 1.5 * inch, 1.5 * inch]
    )
    items_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                (
                    "ALIGN",
                    (0, 1),
                    (0, -1),
                    "LEFT",
                ),  # Product names left-aligned
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    elements.append(items_table)
    elements.append(Spacer(1, 20))

    # Order totals
    tax = subtotal * Decimal("0.08")  # 8% tax

    totals_data = [
        ["Subtotal:", f"${subtotal:.2f}"],
        ["Tax (8%):", f"${tax:.2f}"],
        ["Total:", f"${order.total_amount:.2f}"],
    ]

    totals_table = Table(totals_data, colWidths=[4.5 * inch, 1.5 * inch])
    totals_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, -1), (-1, -1), 12),
                ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(totals_table)
    elements.append(Spacer(1, 30))

    # Footer
    elements.append(Paragraph("Thank you for your business!", styles["Normal"]))
    elements.append(
        Paragraph(
            (
                "For questions about this invoice, please contact us at "
                "support@himalayanecommerce.com"
            ),
            styles["Normal"],
        )
    )

    # Build PDF
    doc.build(elements)

    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data


def send_order_confirmation_email(order):
    """Send order confirmation email with PDF invoice attachment."""
    try:
        # Generate invoice PDF
        pdf_data = generate_invoice_pdf(order)

        # Prepare email context
        # Determine recipient and customer object for templates
        buyer = getattr(order, "buyer", None)
        recipient_email = (
            buyer.email if buyer and getattr(buyer, "email", None) else order.guest_email
        )

        context = {
            "order": order,
            "customer": buyer or {
                "name": order.guest_name,
                "email": order.guest_email,
            },
            "order_items": order.items.all(),
            "subtotal": sum(item.price * item.quantity for item in order.items.all()),
            "tax": order.total_amount * Decimal("0.08") / Decimal("1.08"),
            "total": order.total_amount,
        }

        # Render email templates
        html_content = render_to_string(
            "shop/emails/order_confirmation.html",
            context,
        )
        text_content = strip_tags(html_content)

        # Create email
        subject = "Order Confirmation - {oid} - Himalayan eCommerce".format(
            oid=order.order_id
        )

        from_email = getattr(
            settings,
            "DEFAULT_FROM_EMAIL",
            "noreply@himalayanecommerce.com",
        )
        # Fall back to guest email when buyer is not present
        to_email = [recipient_email] if recipient_email else []

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            to_email,
        )
        msg.attach_alternative(html_content, "text/html")

        # Attach PDF invoice
        msg.attach(
            f"Invoice_{order.order_id}.pdf",
            pdf_data,
            "application/pdf",
        )

        # Send email
        if to_email:
            msg.send()
        else:
            logger.warning(
                "No recipient email available for order %s; skipping send",
                order.order_id,
            )

        logger.info(
            "Order confirmation email sent successfully for order %s",
            order.order_id,
        )
        return True
    except Exception as e:  # pylint: disable=broad-except
        # Use logger.exception to include traceback and avoid f-string interpolation
        logger.exception(
            "Failed to send order confirmation email for order %s: %s",
            order.order_id,
            e,
        )
        return False


def send_order_status_update_email(order, old_status, new_status):
    """Send email notification when order status changes."""
    try:
        context = {
            "order": order,
            "customer": order.buyer,
            "old_status": old_status,
            "new_status": new_status,
        }

        # Render email templates
        html_content = render_to_string(
            "shop/emails/order_status_update.html",
            context,
        )
        text_content = strip_tags(html_content)

        # Create email
        subject = "Order Status Update - {oid} - Himalayan eCommerce".format(
            oid=order.order_id
        )

        from_email = getattr(
            settings,
            "DEFAULT_FROM_EMAIL",
            "noreply@himalayanecommerce.com",
        )
        to_email = [order.buyer.email]

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            to_email,
        )
        msg.attach_alternative(html_content, "text/html")

        # Send email
        msg.send()

        logger.info(
            "Order status update email sent for order %s",
            order.order_id,
        )
        return True
    except Exception as e:  # pylint: disable=broad-except
        logger.exception(
            "Failed to send order status update email for order %s: %s",
            order.order_id,
            e,
        )
        return False
