import openai
import os
import mysql.connector
from mysql.connector import Error
from decouple import config


MYSQL_PW = '/run/secrets/mysql_pw'
OAI_ORG = config('OAI_ORG')
OAI_API = config('OAI_API')
# IP_ADDR = config('IP_ADDR')

openai.organization = OAI_ORG
openai.api_key = OAI_API

def check_openai():
    response = openai.Completion.create(
    model="code-davinci-002",
    prompt="### MySQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query to list the names of the departments which employed more than 10 employees in the last 3 months\nSELECT",
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["#", ";"]
    )
    print(response['choices'][0]['text'])



try:
    print(f'Databases available: sakila, world_x')
    port_input = input('Select Database: ')
    if port_input == 'sakila':
        port_no='3306'
        db_input='sakila'
    elif port_input == 'world_x':
        port_no='3307'
        db_input='world_x'
except IOError:
    print(f'Error: input not recognizable')

def connect_mysql():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       port=port_no,
                                       database=db_input,
                                       user='vscode',
                                       password=MYSQL_PW)
        if conn.is_connected():
            print(f'Connected to MySQL database: {db_input}')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()




def fetch_tables():
    mydb = mysql.connector.connect(
        host='localhost',
        port=port_no,
        user="vscode",
        password=MYSQL_PW,
        database=db_input
        )

    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    myresult = mycursor.fetchall()
    #extract name of columns only from output
    columns={}
    for i in range(len(list(myresult))):
        table_name = myresult[i][0]
        query = 'SHOW COLUMNS FROM ' + table_name
        # print(query)
        mycursor.execute(query)
        result = mycursor.fetchall()

        for j in range(len(result)):
            val_list = []
            val = result[j][0]
            if table_name in columns:
                columns[table_name].append(val)
            else:
                val_list.append(val)
                columns[table_name] = val_list

    string_format = "### MySQL tables, with their properties:\n#\n# "
    for k,v in columns.items():
        string_format += (k + '(')
        for i in range(len(v)):
            string_format += (v[i])
            if i == (len(v)-1):
                string_format += ')\n# '
            else: 
                string_format += ', '
    string_format += '\n### A query to '
    user_input = input('Enter your query request: ')
    string_format += (user_input + '\nSELECT')

    ret = openai.Completion.create(
        model="code-davinci-002",
        prompt=string_format,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
        )
    mysql_request = 'SELECT' + ret['choices'][0]['text']

            # print(v[i])
    # print(string_format)
    # print(mysql_request)
    mycursor.execute(mysql_request)
    myresult = mycursor.fetchall()
    print(myresult)
    


def main():
    # check_openai()
    # select_db()
    connect_mysql()
    fetch_tables()

if __name__== "__main__":
    main()
