from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm


def generate_delivery_order(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 13)
    c.drawString(100, height - 45, "MATSU GLOBAL LOGISTICS PVT LTD")
    c.setFont("Helvetica", 9)
    c.drawString(100, height - 60, "NO 49 ( 26 ) MOULA MANOR 4TH FLOOR,")
    c.drawString(100, height - 72, "CORAL MERCHANT STREET, CHENNAI 600001")

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 100, "DELIVERY ORDER")

    # Extended Attention/Details Box
    box_top = height - 115
    box_left = 30
    box_width = width - 60
    box_height = 340  # Extended height to fit all content
    c.rect(box_left, box_top - box_height, box_width, box_height)

    # Left: Attention to (multi-line)
    c.setFont("Helvetica", 9)
    c.drawString(box_left + 10, box_top - 20, "Attention to :-")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + 80, box_top - 20, "xyz")
    c.setFont("Helvetica", 9)
    c.drawString(box_left + 80, box_top - 32, "xyz")
    c.drawString(box_left + 80, box_top - 44, "xyz")
    c.drawString(box_left + 80, box_top - 56, "xyz")

    # Right: DO No and Date
    c.setFont("Helvetica", 9)
    c.drawString(box_left + box_width - 120, box_top - 20, "DO No :")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + box_width - 70, box_top - 20, "xyz")
    c.setFont("Helvetica", 9)
    c.drawString(box_left + box_width - 120, box_top - 32, "Date :")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left + box_width - 70, box_top - 32, "xyz")

    # Details (2 columns)
    c.setFont("Helvetica", 9)
    details_left = [
        ("Please deliver to", "xyz"),
        ("Consignee", "xyz"),
        ("Importer Code/Type", "xyz"),
        ("Notify party", "xyz"),
        ("CHA", "xyz"),
        ("Vessel/Voyage", "xyz"),
        ("O.Bill of Lading", "xyz"),
        ("H.Bill of Lading", "xyz"),
        ("Load Port HBL", "xyz"),
        ("ETA", "xyz"),
        ("IGM No./Date", "xyz"),
        ("Unstuff Place", "xyz"),
    ]
    y = box_top - 70
    for label, value in details_left:
        c.drawString(box_left + 20, y, f"{label} :")
        c.drawString(box_left + 120, y, value)
        y -= 14

    # Table (Container details) - now inside the box
    table_data = [
        ["Container No.", "LCL/FCL", "Unstuff Dt.", "No of Pkg", "Weight in Kgs", "Volume"],
        ["xyz", "xyz", "xyz", "xyz", "xyz", "xyz"]
    ]
    table = Table(table_data, colWidths=[90, 50, 70, 70, 80, 50], rowHeights=18)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
    ]))
    table.wrapOn(c, width, height)
    table_y = box_top - box_height + 60  # Place table inside the box, leaving space for details
    table.drawOn(c, box_left, table_y)

    # Marks, Description, Note (inside the box, below the table)
    c.setFont("Helvetica", 9)
    c.drawString(box_left, table_y - 25, "Marks & Nos :  xyz")
    c.drawString(box_left, table_y - 40, "Description :  xyz")
    c.drawString(box_left, table_y - 65, "Dear Sir,")
    c.setFont("Helvetica", 8)
    c.drawString(box_left, table_y - 80, "Please note this Delivery Order is valid for 30 days from the vessel arrival date. Thereafter reissue due to loss of original DO or exceeding the validity of aforesaid 30 days will incur additional charges of INR 1000 for every additional 10 days.")

    # Footer
    c.setFont("Helvetica-Bold", 9)
    c.drawString(box_left, 90, "For     MATSU GLOBAL LOGISTICS PVT LTD")
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 60, '"This Delivery order is subject to the terms and conditions of the relative B/L"')
    c.setFont("Helvetica", 7)
    c.drawString(box_left, 45, "Ref: xyz on xyz by xyz")
    c.drawRightString(width - 30, 45, "Page 1 of 1")

    c.save()

if __name__ == "__main__":
    generate_delivery_order("delivery_order_sample.pdf") 