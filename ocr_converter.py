import pdf2image
import pytesseract
from PIL import Image
from flask import Flask, request
import re
import json

app = Flask(__name__)

def convert_pdf_to_images(file):
    images = pdf2image.convert_from_bytes(file.read())
    return images

def perform_ocr_on_image(image):
    ocr_text = pytesseract.image_to_string(image)
    return ocr_text

def format_ocr_text(ocr_text, page_number):
    formatted_text = ""
    if page_number == 1:
        formatted_text += "\n\n"  # Add two new lines before the page number for the first page
    formatted_text += f"Page {page_number}:\n"  # Add the page number at the beginning
    formatted_text += ocr_text.replace('\n', ' ')
    return formatted_text

def process_pdf_text(text):
    patterns = {
    "invoice_number": r"Invoice Number[^:]*: ([^; ]+)",
    "invoice_number_confidence": r"INCHN[^:]*: ([^; ]+)",
    "invoice_date": r"(\d{2}\.\d{2}\.\d{4})",
    "org_invoice_no": r"Invoice Number[^:]*: ([^; ]+)",
    "document_type": r"Type[^:]*: ([^; ]+)",
    "total_amount": r"Total Invoice Value \(In Figure\) ([0-9,.]+)",
    "eway_bill_no": r"E-Way Bill No.[^:]*: ([^; ]+)",
    "eway_bill_date": r"(\d{2}\.\d{2}\.\d{4})",
    "po_number": r"PO[^:]*: ([^; ]+)",
    "po_date": r"(\d{2}\.\d{2}\.\d{4})",
    "grn_no": r"Grn No [^:]*: ([^; ]+)",
    "grn_date": r"(\d{2}\.\d{2}\.\d{4})",
    "due_date": r" (\d{2}\.\d{2}\.\d{4})",
    "irn_no": r"IRN\s*\s*([^ ]+) | IRN :\s*\s*([^ ]+)",
    "freight_amount": r"Freight Amt [^:]*: ([^; ]+)",
    "freight_tax": r"Freight Tax [^:]*: ([^; ]+)",
    "currency": r"\b(AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|FJD|FKP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|IMP|INR|IQD|IRR|ISK|JEP|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|UAH|UGX|UYU|UZS|VEF|VND|VUV|WST|XAF|XCD|XDR|XOF|XPF|YER|ZAR|ZMW)\b",
    "supplier_code": r"Supplier Code[^:]*: ([^; ]+)",
    "supplier_name": r"([A-Z=\s&]+)(?:LIMITED|PVT LTD|PRIVATE LIMITED)",
    "supplier_address": r"CEAT LIMITED - HALOL PLANT\s*([^:]+?)(?=GSTIN)",
    "supplier_gstin": r"GSTIN No.\s*:\s*([^ ]+)",
    "supplier_pan_number": r"PAN No.\s*:\s*([^ ]+)",
    "supplier_email": r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$",
    "customer_name": r"Name\s*:\s*([^:]+)\s*Address",
    "customer_address": r"Address\s*:\s*([^:]+?)(?=Place of Supply)",
    "customer_gstin": r"GSTIN\s*:\s*([^ ]+)",
    "customer_pan_number": r"PAN No.\s*:\s*([^ ]+)",
    "customer_email": r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$",
    "taxable_amount": r"Taxable Value(Rs.)[^:]*: ([^; ]+)",
    "cgst_rate": r"Rate(%)Total[^:]*: ([^; ]+)",
    "cgst_amount": r"Amt.(Rs.)[^:]*: ([^; ]+)",
    "sgst_rate": r"Rate(%)[^:]*: ([^; ]+)",
    "sgst_amount": r"Amt.(Rs.)[^:]*: ([^; ]+)",
    "igst_rate": r"Rate(%)[^:]*: ([^; ]+)",
    "igst_amount": r"Amt.(Rs.)[^:]*: ([^; ]+)",
    "ugst__rate": r"Ugst[^:]*: ([^; ]+)",
    "ugst_amount": r"Ust Amt [^:]*: ([^; ]+)",
    "cess_amount": r"Cess amt[^:]*: ([^; ]+)",
    "total_inv_amount": r"Total Invoice Value \(In Figure\)\s*([^ ]+)",
    "main_hsn_code": r"Main Hsn Code [^:]*: ([^; ]+)",
    "total_line_items": r"TLI [^:]*: ([^; ]+)",
    "invoice line item details": {
        "serial_no": r"Sr. No[^:]*: ([^; ]+)",
        "hsn_code": r"HSN No.[^:]*: ([^; ]+)",
        "description": r"Description[^:]*: ([^; ]+)",
        "quantity": r"Qty.[^:]*: ([^; ]+)",
        "unitprice": r"Unit[^:]*: ([^; ]+)",
        "cgst_rate": r"Rate(%)Total[^:]*: ([^; ]+)",
        "cgst_amount": r"Amt.(Rs.)[^:]*: ([^; ]+)",
        "sgst_rate": r"Rate(%)[^:]*: ([^; ]+)",
        "sgst_amount": r"Amt.(Rs.)[^:]*: ([^; ]+)",
        "igst_rate": r"Rate(%)[^:]*: ([^; ]+)",
        "igst_amount": r"Amt.(Rs.)[^:]*: ([^; ]+)",
        "total_item_amount": r"Total Invoice Value \(In Figure\)\s*([^ ]+)",
    }
    
}

    data = {}

    for key, pattern in patterns.items():
        if isinstance(pattern, dict):
            sub_data = {}
            for sub_key, sub_pattern in pattern.items():
                result = re.search(sub_pattern, text)
                if result:
                    sub_data[sub_key] = result.group(1)
            data[key] = sub_data
        else:
            result = re.search(pattern, text)
            if result:
                data[key] = result.group(1)

    json_data = json.dumps(data, indent=4)
    return json_data

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return 'No file uploaded.'
    
    file = request.files['file']
    if file.filename == '':
        return 'Empty filename.'

    try:
        images = convert_pdf_to_images(file)
    except Exception as e:
        return f'Error converting PDF to images: {str(e)}'

    formatted_ocr_text = ""
    for i, image in enumerate(images):
        ocr_text = perform_ocr_on_image(image)
        formatted_ocr_text += format_ocr_text(ocr_text, i+1)
        formatted_ocr_text += "\n\n"  # Add two new lines after each page

    processed_data = process_pdf_text(formatted_ocr_text)

    return processed_data

if __name__ == '__main__':
    app.run(port=5001)
