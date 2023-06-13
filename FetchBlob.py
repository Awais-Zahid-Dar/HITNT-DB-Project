import mysql.connector
from mysql.connector import Error
import os.path


def write_file(data, filename):

    save_path = 'D:\Face-Recognition-Login-System-main\Images'
    completeName = os.path.join(save_path, filename)
    # Convert binary data to proper format and write it on Hard Disk
    with open(completeName, 'wb') as file:
        file.write(data)

def readBLOB(emp_id, photo):
    print("Reading BLOB data from python_employee table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='keto_shop',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT Picture from user where uid = %s"""

        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()
        for row in record:
            
            image = row[-1]
            print("Storing employee image and bio-data on disk \n")
            write_file(image, photo)

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
