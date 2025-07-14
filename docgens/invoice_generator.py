from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def create_invoice():
    """
    Creates a PDF invoice based on a predefined template.
    The data is currently hardcoded with placeholders.
    """
    doc = SimpleDocTemplate("invoice.pdf", pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    story = []
    styles = getSampleStyleSheet()

    # Placeholder Data
    data = {
        "company_name": "MATSU",
        "company_address": "BANGALORE FF<br/>3rd, 2M-210, VP Towers, 2nd Main, East of NGEF Layout,<br/>Kasturi Nagar, Bengaluru, Bengaluru Urban, Karnataka, 560043",
        "invoice_title": "STATEMENT OF CHARGES/PRO-FORMA INVOICE",
        "job_no": "ABC-12345",
        "date": "01-JAN-25",
        "to_name": "Global Imports Inc.",
        "to_address": "456 International Drive, Suite 100<br/>New York, NY 10001, USA",
        "to_gst": "N/A",
        "to_pan": "N/A",
        "vessel": "Oceanic Voyager",
        "carrier": "SeaLink Shipping",
        "voyage_no": "OV-300",
        "obl": "SLS-987654321",
        "hbl": "GII-54321",
        "commodity": "Assorted Machine Parts",
        "pol": "SHANGHAI",
        "pod": "NEW YORK",
        "fdc": "NEW YORK",
        "salesman": "John Doe",
        "shipper_ref": "SH-54321",
        "shipper_name": "Export Goods Co. Ltd.",
        "consignee_name": "Global Imports Inc.",
        "containers": [
            ["20FT", "CONT1234567", "500", "10000.000", "33.000"],
            ["40FT", "CONT7654321", "1000", "20000.000", "67.000"],
            ["20FT", "CONT2468135", "550", "11000.000", "33.000"],
        ],
        "charges": [
            ["1", "OCEAN FREIGHT", "2.000", "2,500.00", "USD", "83.500000", "5000.00", "417500.000", ""],
            ["2", "TERMINAL HANDLING", "2.000", "500.00", "USD", "83.500000", "1000.00", "83500.000", ""],
            ["3", "DOCUMENT FEE", "1.000", "150.00", "USD", "83.500000", "150.00", "12525.000", ""],
            ["4", "CUSTOMS CLEARANCE", "1.000", "300.00", "USD", "83.500000", "300.00", "25050.000", ""],
            ["5", "INLAND HAULAGE", "1.000", "1,200.00", "USD", "83.500000", "1200.00", "100200.000", ""],
            ["6", "SERVICE TAX @ 18%", "", "", "INR", "1.000000", "115000.00", "115000.00", ""],
            ["7", "", "", "", "", "", "", "", ""],
            ["8", "", "", "", "", "", "", "", ""],
            ["9", "", "", "", "", "", "", "", ""],
        ],
        "total": "753775.000",
        "amount_in_words": "Seven Hundred Fifty-Three Thousand Seven Hundred Seventy-Five RUPEES Only",
        "pan_no_footer": "ABCDE1234F",
        "note": "Sample invoice with different data.",
        "ref_footer": "Ref: S-00123 on 01-JAN-2025 by YOURCOMPANY-LOCATION",
    }
    
    # Custom Styles
    styles.add(ParagraphStyle(name='LeftBold', alignment=0, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Right', alignment=2))
    styles.add(ParagraphStyle(name='RightBold', alignment=2, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='CenterBold', alignment=1, fontName='Helvetica-Bold', fontSize=12))

    # Header
    header_data = [
        [Paragraph('<b>' + data["company_name"] + '</b>', styles['Normal']), '', Paragraph(data["invoice_title"], styles['CenterBold'])],
        [Paragraph(data["company_address"], styles['Normal']), '', ''],
        ['', '', Paragraph(f'Job No : {data["job_no"]} / {data["date"]}', styles['Right'])]
    ]
    header_table = Table(header_data, colWidths=[2.5*inch, 2*inch, 3*inch])
    header_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 1), (1, 1)),
        ('SPAN', (2, 0), (2, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.2*inch))

    # To / Shipment Details
    to_details_data = [
        [Paragraph('To :', styles['Normal']), Paragraph(data['to_name'], styles['LeftBold'])],
        ['', Paragraph(data['to_address'], styles['Normal'])],
        [Paragraph('GST ID :', styles['Normal']), data['to_gst'] + ' State Code :'],
        [Paragraph('PAN NO:', styles['Normal']), data['to_pan']],
        [Paragraph('Vessel', styles['Normal']), Paragraph(f": {data['vessel']}", styles['Normal'])],
        [Paragraph('Carrier', styles['Normal']), Paragraph(f": {data['carrier']}", styles['Normal'])],
        [Paragraph('Voyage/Flight no', styles['Normal']), Paragraph(f": {data['voyage_no']}", styles['Normal'])],
        [Paragraph('OBL', styles['Normal']), Paragraph(f": {data['obl']}", styles['Normal'])],
        [Paragraph('HBL', styles['Normal']), Paragraph(f": {data['hbl']}", styles['Normal'])],
        [Paragraph('Commodity', styles['Normal']), Paragraph(f": {data['commodity']}", styles['Normal'])],
    ]
    to_details_table = Table(to_details_data, colWidths=[1.2*inch, 6*inch])
    to_details_table.setStyle(TableStyle([
       ('VALIGN', (0, 0), (-1, -1), 'TOP'),
       ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(to_details_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Container Table
    container_header = [['', 'Container', 'Pcs', 'Weight', 'Volume']]
    container_data = container_header + data['containers']
    container_table = Table(container_data, colWidths=[0.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
    container_table.setStyle(TableStyle([
        ('BOX', (1, 0), (-1, -1), 1, colors.black),
        ('GRID', (1, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (1, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (1, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(container_table)
    story.append(Spacer(1, 0.2*inch))

    # POL/POD/Salesman
    pol_pod_data = [
        [Paragraph('POL', styles['Normal']), Paragraph(f": {data['pol']}", styles['Normal']), Paragraph('Salesman Name', styles['Normal']), Paragraph(f": {data['salesman']}", styles['Normal'])],
        [Paragraph('POD', styles['Normal']), Paragraph(f": {data['pod']}", styles['Normal']), Paragraph('Shipper Ref No', styles['Normal']), Paragraph(f": {data['shipper_ref']}", styles['Normal'])],
        [Paragraph('FDC', styles['Normal']), Paragraph(f": {data['fdc']}", styles['Normal']), '', ''],
    ]
    pol_pod_table = Table(pol_pod_data, colWidths=[1*inch, 2.5*inch, 1.5*inch, 2.5*inch])
    pol_pod_table.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0)]))
    story.append(pol_pod_table)
    story.append(Spacer(1, 0.1*inch))
    
    # Shipper/Consignee
    shipper_data = [
        [Paragraph('Shipper Name', styles['Normal']), Paragraph(f": {data['shipper_name']}", styles['Normal'])],
        [Paragraph('Consignee Name', styles['Normal']), Paragraph(f": {data['consignee_name']}", styles['Normal'])],
    ]
    shipper_table = Table(shipper_data, colWidths=[1.5*inch, 6*inch])
    shipper_table.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0)]))
    story.append(shipper_table)
    story.append(Spacer(1, 0.2*inch))

    # Charges Table
    story.append(Paragraph("COLLECT CHARGES", styles['CenterBold']))
    story.append(Spacer(1, 0.1*inch))
    charges_header = [['SNo', 'Charge Name', 'Volume', 'Per Unit', 'Currency', 'ROE', 'Amount', 'In INR', 'TAX']]
    charges_data = charges_header + data['charges']
    charges_table = Table(charges_data, colWidths=[0.4*inch, 2*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.9*inch, 0.8*inch, 1*inch, 0.4*inch])
    charges_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'), # Charge Name column
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(charges_table)
    story.append(Spacer(1, 0.1*inch))

    # Total
    total_data = [['', Paragraph(f'Total :   {data["total"]}', styles['RightBold'])]]
    total_table = Table(total_data, colWidths=[5.5*inch, 2*inch])
    story.append(total_table)
    story.append(Spacer(1, 0.2*inch))

    # Amount in words
    story.append(Paragraph(data['amount_in_words'], styles['Normal']))
    story.append(Spacer(1, 0.4*inch))

    # Footer
    story.append(Paragraph(f'PAN No: {data["pan_no_footer"]}', styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f'Note : {data["note"]}', styles['Normal']))
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph(data['ref_footer'], styles['Normal']))

    doc.build(story)

if __name__ == '__main__':
    create_invoice()
    print("Invoice 'invoice.pdf' generated successfully.") 