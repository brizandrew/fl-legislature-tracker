#!/usr/bin/env python3
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup

try: 
    conn = pymysql.connect(host='127.0.0.1', unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock', user='root', passwd=None, db='flbilltrack')
    cur = conn.cursor()
    cur.execute("USE flbilltrack")


    html = urlopen("https://www.flsenate.gov/Senators")
    bsObj = BeautifulSoup(html, "html.parser")

    tbody = bsObj.find("table",{"id":"Senators"}).tbody
    table = tbody.findAll("tr")

    for row in table:
        name = row.find("th").getText().strip()
        lname = name[:name.index(",")]
        fname = name[name.index(",")+2:]
        district = row.findAll("td")[0].getText().strip()
        partyText = row.findAll("td")[1].getText().strip()

        if partyText == "Democrat":
            party = "D"
        elif partyText == "Republican":
            party = "R"

        countyText = row.findAll("td")[2].getText().strip()
        county = countyText[12:]
        cur.execute("INSERT INTO senators(fname,lname,district,party,county) VALUES(%s,%s,%s,%s,%s)", (fname, lname, district, party, county))
        cur.connection.commit()
    cur.close()
finally:
    conn.close()