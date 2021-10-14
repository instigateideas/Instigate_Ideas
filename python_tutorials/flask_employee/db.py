import pymysql


username = "arunachalam"
password = "Mypassword@123"
database_name = "employee"


def establish_connection():
    try:
        connection = pymysql.connect(host='localhost', user=username,
                                     password=password, database=database_name,
                                     cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        connection = None
        print("Error while establishing connection...")

    return connection



