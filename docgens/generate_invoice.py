import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from functools import partial

def get_invoice_data(cursor, invoice_id):
    cursor.execute('''SELECT company_logo, company_name, company_address, document_title, notify_party, consignee, shipper, sales_ref, \
        job_ref_no, invoice_ref, igm_dt, from_field, shipment_details, po_no, hbl_no, vsl_voy, booking_no, service, obl_no, obl_date, origin, pol, pod, eta, final_dest, warehouse, item_no, sub_item_no, all_prepaid, carrier_name, total_usd, total_inr, pan_no, notes, \
        frt_amount, exw_amount, dtd_date, stamp_image
        FROM invoices WHERE id = ?''', (invoice_id,))
    row = cursor.fetchone()
    if not row:
        print('Invoice not found!')
        return None
    return row

def get_invoice_items(cursor, invoice_id):
    cursor.execute('''SELECT marks_numbers, description, container, seal, ctn, weight, volume FROM invoice_items WHERE invoice_id = ?''', (invoice_id,))
    return cursor.fetchall()

def get_invoice_charges(cursor, invoice_id):
    cursor.execute('''SELECT charge, curr, units, per_unit, amount, roe, amt_inr, tax FROM invoice_charges WHERE invoice_id = ?''', (invoice_id,))
    return cursor.fetchall()

def draw_stamp(stamp_path, canvas, doc):
    if canvas.getPageNumber() == 2:
        canvas.saveState()
        if stamp_path:
            try:
                x_pos = 450
                y_pos = 650
                canvas.drawImage(stamp_path, x_pos, y_pos, width=100, height=100, mask='auto')
            except Exception as e:
                print(f"Warning: Could not draw stamp image '{stamp_path}'. Error: {e}")
        canvas.restoreState()

def generate_invoice(filename, invoice_id):
    db_path = 'invoices.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    row = get_invoice_data(cursor, invoice_id)
    if not row:
        raise ValueError('Invoice not found!')
    (
        company_logo, company_name, company_address, document_title, notify_party, consignee, shipper, sales_ref,
        job_ref_no, invoice_ref, igm_dt, from_field, shipment_details, po_no, hbl_no, vsl_voy, booking_no, service, obl_no, obl_date, origin, pol, pod, eta, final_dest, warehouse, item_no, sub_item_no, all_prepaid, carrier_name, total_usd, total_inr, pan_no, notes,
        frt_amount, exw_amount, dtd_date, stamp_image
    ) = row

    items = get_invoice_items(cursor, invoice_id)
    charges = get_invoice_charges(cursor, invoice_id)

    left_info = [
        [Paragraph('<b>Notify Party (Broker) :</b>', None)],
        [Paragraph((notify_party or '').replace('\n', '<br/>'), None)],
        [Paragraph('<b>Consignee :</b>', None)],
        [Paragraph((consignee or '').replace('\n', '<br/>'), None)],
        [Paragraph('<b>Shipper :</b>', None)],
        [Paragraph((shipper or '').replace('\n', '<br/>'), None)],
        [Paragraph(f'<b>Sales Ref. :</b> {sales_ref or ""}', None)]
    ]
    right_fields = [
        ('Job Ref No', job_ref_no), ('Invoice Ref', invoice_ref), ('IGM Dt', igm_dt), ('From', from_field), ('Shipment Details', shipment_details),
        ('PO #', po_no), ('HBL No', hbl_no), ('Vsl/Voy', vsl_voy), ('Booking No', booking_no), ('Service', service),
        ('OBL No', obl_no), ('OBL Date', obl_date), ('Origin', origin), ('POL', pol), ('POD', pod), ('ETA', eta),
        ('Final Dest', final_dest), ('Warehouse', warehouse), ('Item No', item_no), ('Sub Item No', sub_item_no),
        ('All prepaid', all_prepaid), ('Carrier Name', carrier_name)
    ]
    right_info = [[Paragraph(f'<b>{label} :</b>', None), value or ''] for label, value in right_fields]

    table_items = [["Marks & Numbers", "Description", "Container", "Seal", "CTN", "Weight", "Volume"]]
    for item in items:
        table_items.append(list(item))
    try:
        total_ctn = str(sum(float(i[4]) for i in items if i[4]))
        total_weight = str(sum(float(i[5]) for i in items if i[5]))
        total_volume = str(sum(float(i[6]) for i in items if i[6]))
    except Exception:
        total_ctn = total_weight = total_volume = ''
    table_items.append(["", "", "", "<b>Total :</b>", total_ctn, total_weight, total_volume])

    table_charges = [["Charge", "Curr", "Units", "Per Unit", "Amount", "ROE", "Amt(INR)", "Tax"]]
    for charge in charges:
        table_charges.append(list(charge))

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleB = ParagraphStyle(name='Bold', parent=styleN, fontName='Helvetica-Bold')
    style_center = ParagraphStyle(name='center', parent=styleN, alignment=TA_CENTER)
    style_left = ParagraphStyle(name='left', parent=styleN, alignment=TA_LEFT)

    def local_draw_stamp(canvas, doc):
        draw_stamp(stamp_image, canvas, doc)

    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = []

    header_table_data = []
    if company_logo:
        try:
            logo_img = Image(company_logo, width=60, height=30)
            header_table_data.append([logo_img, Paragraph(f"<b>{company_name}</b><br/>{company_address.replace(chr(10), '<br/>')}", styleN)])
        except Exception:
            header_table_data.append(["", Paragraph(f"<b>{company_name}</b><br/>{company_address.replace(chr(10), '<br/>')}", styleN)])
    else:
        header_table_data.append(["", Paragraph(f"<b>{company_name}</b><br/>{company_address.replace(chr(10), '<br/>')}", styleN)])
    header_table = Table(header_table_data, colWidths=[70, 380])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(KeepTogether([header_table]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"<b>{document_title}</b>", style_center))
    elements.append(Spacer(1, 10))

    left_table = Table(left_info, colWidths=[180])
    left_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    right_table = Table(right_info, colWidths=[70, 120])
    right_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    info_table = Table([[left_table, right_table]], colWidths=[200, 250])
    info_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (1,0), (1,0), 0.5, colors.black),
    ]))
    elements.append(KeepTogether([info_table]))
    elements.append(Spacer(1, 10))

    item_table = Table(table_items, colWidths=[60, 120, 70, 40, 50, 60, 60])
    item_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('SPAN', (0,len(table_items)-1), (2,len(table_items)-1)),
        ('ALIGN', (3,len(table_items)-1), (3,len(table_items)-1), 'RIGHT'),
        ('FONTNAME', (3,len(table_items)-1), (3,len(table_items)-1), 'Helvetica-Bold'),
    ]))
    elements.append(KeepTogether([item_table]))
    elements.append(Spacer(1, 8))

    charges_table = Table(table_charges, colWidths=[60, 30, 35, 35, 45, 45, 60, 30])
    charges_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    elements.append(KeepTogether([charges_table]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"<b>Total(USD):</b> {total_usd}    <b>Total(INR):</b> {total_inr}", style_left))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"PAN No : {pan_no}", styleN))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(notes or '', styleN))

    elements.append(PageBreak())

    elements.append(KeepTogether([header_table]))
    elements.append(Spacer(1, 12))

    cert_title_style = ParagraphStyle(name='cert_title', parent=style_center, spaceAfter=20)
    elements.append(Paragraph("TO WHOM SO EVER IT MAY CONCERN", cert_title_style))
    elements.append(Paragraph("<b>FREIGHT CERTIFICATE</b>", cert_title_style))
    elements.append(Spacer(1, 24))

    body_style = ParagraphStyle(name='body_style', parent=styleN, fontSize=11, leading=16, spaceAfter=12)
    elements.append(Paragraph(f"This is to inform you that freight & Exworks Amount for", body_style))
    elements.append(Paragraph(f"Shippment moved under HBL/HAWB {hbl_no or ''} is", body_style))
    elements.append(Paragraph(f"Dtd : {dtd_date or ''}", body_style))
    elements.append(Paragraph(f"FRT: {frt_amount or ''}", body_style))
    elements.append(Paragraph(f"EXW : {exw_amount or ''}", body_style))
    elements.append(Spacer(1, 80))

    sig_table_data = [
        ['NVOCC)', 'MATSU GLOBAL LOGISTICS PVT LTD (BLR)'],
        ['', ''],
        ['', 'Operation Team']
    ]
    sig_table = Table(sig_table_data, colWidths=[225, 225])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    elements.append(sig_table)

    doc.build(elements, onPage=local_draw_stamp)

if __name__ == "__main__":
    import sys
    invoice_id = 1
    if len(sys.argv) > 1:
        invoice_id = int(sys.argv[1])
    generate_invoice("invoice_output.pdf", invoice_id) 