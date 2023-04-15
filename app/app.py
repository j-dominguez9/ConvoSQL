import openai
import os
import mysql.connector
from mysql.connector import Error
from decouple import config
import streamlit as st
import pandas as pd

st.set_page_config(page_title="MySQL Translator")

MYSQL_PW = '/run/secrets/mysql_pw'
OAI_ORG = config('OAI_ORG')
OAI_API = config('OAI_API')
# IP_ADDR = config('IP_ADDR')

openai.organization = OAI_ORG
openai.api_key = OAI_API

def get_port(database):
    if database == 'sakila':
        port_no='3306'
    elif database == 'world_x':
        port_no='3307'
    return port_no


def connect_mysql(database_input, port_number):
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       port=port_number,
                                       database=database_input,
                                       user='vscode',
                                       password=MYSQL_PW)
        if conn.is_connected():
            # print('Connected to MySQL database')
            st.success(f'Connected to MySQL database ({database_input})', icon="✅")
            return conn

    except Error as e:
        # print(e)
        st.error(f'{e}', icon="🚨")

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def show_box():
    form = st.form(key='connect_form')
    db_input = form.selectbox(
    'Select Database',
    ('sakila', 'world_x'))
    submit = form.form_submit_button('Connect')
    port_no = get_port(db_input)
    if submit:
        connect_mysql(db_input, port_no)
    return db_input,port_no

def header():
    st.header(':blue[MySQL] Translator')

def get_columns(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    str = value[adjusted_pos_a:pos_b].replace(",\n", ", ").split(", ")
    # str = str.split(", ")
    str2 = [i.strip() for i in str]
    return str2

def fetch_tables():
    header()
    st.caption('Please connect to database first.')
    db_input, port_no = show_box()

    form = st.form('query')
    user_query = form.text_input('Enter your query request', 'list all tables')
    submit = form.form_submit_button('Query')
    if submit:

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
        # user_input = input('Enter your query request: ')
        # user_input = st.text_input('Enter your query request', 'list all tables')
        # st.write('The current movie title is', title)
        string_format += (user_query + '\nSELECT')

        ret = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates English to SQL code."},
                {"role": "user", "content": string_format}
                ],
            temperature=0,
            max_tokens=150,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["#", ";"]
            )
        text_ret = ret['choices'][0]['message']['content']
        if "SELECT" in text_ret:
            mysql_request = text_ret
        else:
            mysql_request = 'SELECT ' + text_ret
        
        # mysql_request = 'SELECT ' + ret['choices'][0]['message']['content']

                # print(v[i])
        # print(string_format)
        # print(mysql_request)
        st.text(mysql_request)
        columns_request= get_columns(mysql_request, 'SELECT', 'FROM')
        # st.text(columns_request)
        if user_query == "list all tables":
            mysql_request = "SHOW TABLES"
            mycursor.execute(mysql_request)
        else:
            mycursor.execute(mysql_request)
        # mycursor.execute(mysql_request)
        myresult = mycursor.fetchall()
        if columns_request[0] == '*':
            tables = get_columns(mysql_request, 'FROM', 'WHERE')
            myresult = pd.DataFrame(myresult)
            st.text(tables)
        else:
            myresult = pd.DataFrame(myresult, columns = columns_request)
        @st.cache_data
        def convert_df(df):
            return df.to_csv()
        st.dataframe(myresult)
        csv = convert_df(myresult)
        st.download_button(label='Download data as CSV',
                           data = csv,
                           file_name='mysql_data.csv',
                           mime='text/csv')
    # print(myresult)
    



def main():
    fetch_tables()

if __name__== "__main__":
    main()
