#!/usr/bin/env python3
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup

try:
    conn = pymysql.connect(host='127.0.0.1', unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock', user='root', passwd=None, db='flbilltrack')
    cur = conn.cursor()
    cur.execute("USE flbilltrack")


    html = urlopen("http://www.myfloridahouse.gov/Sections/Representatives/representatives.aspx")
    bsObj = BeautifulSoup(html, "html.parser")

    table = bsObj.findAll("div",{"class":"rep_listing1"})

    for row in table:
        district = row.find("div",{"class":"district_style"}).getText().strip()
        party = row.find("div",{"class":"party_style"}).getText().strip()
        name = row.find("div",{"class":"rep_style"}).getText().strip()
        lname = name[:name.index(",")]
        fname = name[name.index(",")+2:]
        county = row.find("div",{"class":"county_style"}).getText().strip()
        cur.execute("INSERT INTO representatives(fname,lname,district,party,county) VALUES(%s,%s,%s,%s,%s)", (fname, lname, district, party, county))
        cur.connection.commit()

    cur.close()

finally:
    conn.close()