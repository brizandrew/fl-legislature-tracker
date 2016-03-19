from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql
import cssutils
import time

try: 

	conn = pymysql.connect(host='127.0.0.1', unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock', user='root', passwd=None, db='flbilltrack')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	cur.execute("USE flbilltrack")

	cur.execute("SELECT id, lname FROM senators")
	cur.connection.commit()
	senators = cur.fetchall()

	cur.execute("SELECT id, lname FROM representatives")
	cur.connection.commit()
	representatives = cur.fetchall()

	for senator in senators:
		cur.execute("SELECT billid FROM votes WHERE congressman = %s and cameral = 'senate'", (senator["lname"]))
		print(senator["lname"], cur.fetchall())
	print("_____________________________")
	for rep in representatives:
		cur.execute("SELECT billid FROM votes WHERE congressman = %s and cameral = 'house'", (rep["lname"]))
		print(rep["lname"], cur.fetchall())

	cur.close()
finally:
	conn.close()
