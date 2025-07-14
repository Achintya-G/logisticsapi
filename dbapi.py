'''
The sturcture of this code is kind of what i want to be consistent through all the other files

-import libraries
-set constants and global stuff
-define the functions that will be called (User defined function)(Focus on making the functions simpler to understand and name them as such and dont make a function to complex)
-define the api endpoints and the corresponding function (api function)
then that last part to actually run the api 


Remember to 
name everything in a consistent manner and the names should be unique and explain what it does
use the underscore (_) to separate words in variable or functions name

also when making the api function (that is the function right below the "db_api.route('/whatever')" ) 
make sure u write the bare minimum code and rather do anything in the user defined functions ( functions written before the db_api.route stuff)
to make it easier to read and understand 





'''


from flask import Flask, request
import psycopg2

db_api = Flask(__name__)

def create_db_from_schema():
    conn = psycopg2.connect(dbname="trial",user="postgres",password="root")
    cur = conn.cursor()
    with open("schema.txt") as f:
        sql_commands = f.read()
        cur.execute(sql_commands)
    conn.commit()
    cur.close()
    conn.close()




def insert_into_table(table,data):
    
    match table:
        case "agent":
            pass
        case "customer":
            print("")
        case "booking":
            print("")

    pass

def update_record_in_table(table,data):

    match table:
        case "agent":
            print("")
        case "customer":
            print("")
        case "booking":
            print("")

    pass

def delete_from_table(table,data):

    match table:
        case "agent":
            print("")
        case "customer":
            print("")
        case "booking":
            print("")
    
    pass

def validate_data(data:dict,table=None):
    print(data)
    match table:
        case "agent":
            print("")
        case "customer":
            print("")
        case "booking":
            print("")
        case None: # Testing case please delete lateer
            for i in data.keys():
                print(f"{i}:{data[i]}({type(data[i])})")

    return True


def search_data(data,table=None):
    match table:
        case "agent":
            print("")
        case "customer":
            print("")
        case "booking":
            print("")
    pass





@db_api.route('/')
def home():

    return '''Make a request to these endpoints.
    Data should be passed in a json format, it will be parsed and validated on the server side of this api

    - docgen_data ['GET']
    - specific_data ['GET']

    - interact customer ['POST','PUT','DELETE']
    - interact agent ['POST','PUT','DELETE']
    - interact booking ['POST','PUT','DELETE']

    - search customer ['GET']
    - search agent ['GET']
    - search booking ['GET']

    '''

@db_api.route('/docgen_data', methods=['GET'])
def docgen_data():
    '''Endpoint that will be accessed only by the docgen service.
    It will return data in a format that the docgen service can use.'''
    if request.method == 'GET':

        return "This is a GET request to the data endpoint."
    

@db_api.route('/specific_data', methods=['GET'])
def specific_data():

    ## most likely will only be a dev feature 
    # lowkey ion even see a use for this now , just leave it empty in the code for now
    '''Endpoint that will be accessed by the user to get specific data.
    It will be used whenever a user queries something that is not written as a specific endpoint.
    the data that will be returned will be whatever the user requested as long as they have the permission to acess it'''
    return "This is a GET request to the specific data endpoint."


### UPDATE ENDPOINTS


@db_api.route('/interact_customer', methods=['POST','PUT','DELETE'])
def interact_customer():
    '''Endpoint to interact with customer table.
    It will be used by the user to add, update or delete customer from the database.'''
    if request.method == 'POST':
        insert_into_table('Customers')
        return 
    elif request.method == 'PUT':
        return "Customer updated sucessfully."
    elif request.method == 'DELETE':
        return "Customer delted sucessfully."
     
@db_api.route('/interact_agent',methods=['POST','PUT','DELETE'])
def interact_agent():
    '''Endpoint to interact with agent table.
    It will be used by the user to add, update or delete agent from then database. 
    '''
    if request.method == 'POST':
        return "Agent added successfully."
    elif request.method == 'PUT':
        return "Agent updated sucessfully."
    elif request.method == 'DELETE':
        return "Agent delted sucessfully."    


    return None


@db_api.route('/interact_booking',methods=['POST','PUT','DELETE'])
def interact_booking():
    '''Endpoint to interact with booking table.
    It will be used by the user to add, update or delete booking from the database.
    '''
    if request.method == 'POST':
        return "Booking added successfully."
    elif request.method == 'PUT':
        return "Booking updated sucessfully."
    elif request.method == 'DELETE':

        return "Booking delted sucessfully."

    return 'make a valid request to this endpoint'


### SEARCH ENDPOINTS (yall gonna have to figure out how to make search and think about what data might be given for a search)       


@db_api.route('/search_customer',methods=['GET'])
def search_customer():
    '''Endpoint to search for customer
    with whatever parameters passed in body of the request.'''

    if request.method == 'GET':
        #u gotta parse the request and its body here and then make a function to do a look up in the db
        return "This is the list of closest results"  # should probably return as a json object


@db_api.route('/search_agent',methods=['GET'])
def search_agent():
    '''Endpoint to search for agent
    with whatever parameters passed in body of the request.'''

    if request.method == 'GET':
        #u gotta parse the request and its body here and then make a function to do a look up in the db
        return "This is the list of closest results"  # should probably return as a json object


@db_api.route('/search_booking',methods=['GET'])
def search_booking():
    '''Endpoint to search for booking
    with whatever parameters passed in body of the request.'''

    if request.method == 'GET':
        #u gotta parse the request and its body here and then make a function to do a look up in the db
        return "This is the list of closest results"  # should probably return as a json object


# ONLY FOR TESTING DELETE LATER
@db_api.route('/test',methods=['GET','POST'])
def test_func():
    '''Endpoint for testing'''

    if request.method == 'POST':
        if request.is_json == True:
            validate_data(data=request.get_json())
            pass
        return "hiii test workde"


if __name__ == "__main__":
    db_api.run(port=5001,debug=True)