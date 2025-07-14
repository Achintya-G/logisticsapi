import psycopg2
import json
from datetime import datetime

def create_db():
    conn = psycopg2.connect(host="localhost",user="postgres",password="root",database="trial")
    cur = conn.cursor()
    with open("schema.txt") as f:
        d=f.read()
        cur.execute(d)
        pass
    cur.close()
    conn.close()


import re

postgresql_to_python = {
    "TEXT":"string",
    "TEXT[]":"list_str",
    "REAL":"float",
    "INTEGER":"int",
    "DATE":"date",
}

def parse_sql_schema(file_path:str) -> dict:

    
    with open(file_path, 'r') as f:
        content = f.read()
    # idek how this works bro regex is scary.
    tables = []
    table_blocks = re.findall(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)

    for table_name, body in table_blocks:
        columns = []
        lines = re.split(r',\s*(?![^()]*\))', body.strip())

        for line in lines:
            line = line.strip()

            if line.upper().startswith("FOREIGN KEY") or "REFERENCES" in line.upper():
                continue

            parts = line.split()
            if len(parts) < 2:
                continue 

            col_name = parts[0]
            col_type = parts[1].upper()
            constraints = ' '.join(parts[2:]).upper()

            is_required = "NOT NULL" in constraints or "PRIMARY KEY" in constraints

            columns.append([col_name, col_type, is_required])

        tables.append([table_name, columns])
    tables_dict = {}
    for i in tables:
        tables_dict[f"{i[0]}"] = i[1:][0]
    return tables_dict


def check_datatype(attributes: list, data: dict) -> bool:
    '''Checks if the data passed is valid with respect to the attributes passed so that it can be entered into a PostgreSQL db'''

    type_map = {
        "SERIAL": None,
        "TEXT": str,
        "JSONB": list,
        "REAL": float,
        "INTEGER": int,
        "DATE": str,  # We'll parse this below
    }

    for attr in attributes:
        col_name, col_type, is_required = attr

        # Check for required fields
        if is_required and col_name not in data:
            print(f"Missing required field: {col_name}")
            return False

        # If field is present, check type
        if col_name in data:
            value = data[col_name]
            expected_type = type_map.get(col_type, str)

            if col_type == "JSONB":
                if not isinstance(value, list):
                    print(f"Field '{col_name}' should be a list of strings")
                    return False
            elif col_type == "DATE":
                if not isinstance(value, str):
                    print(f"Field '{col_name}' should be a string in 'YYYY-MM-DD' format")
                    return False
                try:
                    datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    print(f"Field '{col_name}' should be a valid date in 'YYYY-MM-DD' format")
                    return False
            elif col_type == "SERIAL":
                continue
            elif not isinstance(value, expected_type):
                print(f"Field '{col_name}' should be of type {expected_type.__name__}")
                return False

    return True


def check_json_against_schema(schema_file_path:str,table:str,data:dict=None) -> bool:

    database_schema = parse_sql_schema(schema_file_path)
    if table in database_schema.keys():
        return check_datatype(database_schema[table],data)
    else:
        print("Invalid table name or table schema")
        return False
    


if __name__ == "__main__": 
    agent_data = None
    customer_data = None
    booking_data =None    
    
    with open("agent.json") as f:
        agent_data = json.load(f)
    with open("customer.json") as f:
        customer_data=json.load(f)
        print(customer_data)
    with open("booking.json") as f:
        booking_data=json.load(f)

    print(check_json_against_schema('schema.txt','Agents',agent_data))
    print(check_json_against_schema('schema.txt','Customers',customer_data))
    print(check_json_against_schema('schema.txt','Bookings',booking_data))
    
    pass
