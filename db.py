import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="sign2speak",
    password="sign2speak",
    database="sign2speak"
)

cursor = conn.cursor(dictionary=True)
