import mysql.connector

def get_connection():
    print("USING AWS RDS DATABASE")

    return mysql.connector.connect(
        host="donorconnect-db.c7gmgo0w09eg.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Donor12345",
        database="donorconnect"
    )