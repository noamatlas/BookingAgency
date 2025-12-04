import pyodbc

# print(pyodbc.drivers())

def run_query_sql (query, flag):
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=NITRONOAM\\SQLEXPRESS;"
            "DATABASE=Vacations;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        if flag == "fetch":
            all_records =  cursor.fetchall()
            cursor.close()
            conn.close()
            return all_records #A list of tuples
        else:
            conn.commit()
            cursor.close()
            conn.close()
            return "ok"
    except Exception as e:
        return str(e)


def convert_recordset_to_dict(recordset, col_names):
    data = []
    # columns_names = example: ['ID', 'Name', 'Age', 'Department']
    columns_names = col_names
    for record in recordset:
        record = dict(zip(columns_names, record))
        data.append(record)
    return data

# my_query = "SELECT * FROM Vacations"
# my_flag = "fetch"
# print(run_query_sql(my_query, my_flag))

# my_query = "INSERT INTO Users (userName, email, userPassword, userRole) VALUES ('Menni', 'menni@example.com', 'pass123', 'customer')"
# my_flag = "exec"
# print(run_query_sql(my_query, my_flag))

# my_query = "SELECT * FROM Users"
# my_flag = "fetch"
# users_data = run_query_sql(my_query, my_flag)
# users_cols = ['id', 'userName', 'email', 'userPassword', 'userRole']
# users_dict = convert_recordset_to_dict(users_data, users_cols)
# print(users_dict)