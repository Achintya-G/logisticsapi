from flask import Flask, request


docgen_api = Flask(__name__)


@docgen_api.route('/')
def home():
    return '''
    Make a request to an endpoint with relevant information to get a document generated.
    <hr>
    
    List of endpoints:
    <ul>
    <li>Delivery order template</li>
    <li>Delivery order template</li>
    <li>Delivery order template</li>
    <li>Invoice</li>
    </ul>
    ''' 
    

docgen_api.run(debug=True)