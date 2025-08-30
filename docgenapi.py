from flask import Flask, request ,send_file


docgen_api = Flask(__name__)

def generateInvoice(data):  #this function should be imported


    
    #generate document using the data and save it
    filepath = "/generatedDocuments/invoice567.pdf"

    return filepath

def invoicegen(bookingno):
    # get details using booking number
    data = {"company Name":"Matsu"}

    file_path = generateInvoice(data)

    return 




@docgen_api.route('/')
def home():
    return '''
    Make a request to an endpoint with relevant information to get a document generated.
    <hr>
    
    List of endpoints:
    <ul>
    <li>Delivery order template</li>
    <li>Delivery order template</li>
    <li>Invoice</li>
    </ul>
    ''' 

@docgen_api.route('/invoice')
def invoice():

    # Getting the booking number from the http request
    booking_number=request.json['bookingno']

    # storing the file path after generating
    file_path = invoicegen(bookingno=booking_number)

    # returning the file to the user
    return send_file(file_path, as_attachment=True, download_name=f"{booking_number}Invoice")
    

docgen_api.run(debug=True,port=5003)