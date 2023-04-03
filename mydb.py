# Install Mysql
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python
import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1221',
    auth_plugin='mysql_native_password'
)
cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE phong")
print("All done!")