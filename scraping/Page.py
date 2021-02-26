import requests
import mysql.connector as msc
from bs4 import BeautifulSoup
class Page:

    def __init__(self, url):
        response = requests.get(url)
        self.bs = BeautifulSoup(response.text, 'html.parser')
    
    # Make this an abstract method since the SQL Query will differ depending on position, although connection is the same across all.
    # def send_mysql_data(self):
    #     raise NotImplementedError("Please Implement This Method!")
    def establish_mysql_connection():
        mydb = msc.connect(
            host="capstone-db.cuchsam9yjhs.us-east-1.rds.amazonaws.com",
            user="",
            password=""
        )
        print(mydb.is_connected())
        print("MYSQL CONNECTED")



    


