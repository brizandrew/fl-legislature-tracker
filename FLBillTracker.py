from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql
import time

def scrollToElement(eleId):
	global driver
	driver.execute_script('var element = document.getElementById("'+eleId+'");element.scrollIntoView({block: "end"});')
	element = WebDriverWait(driver, 10).until(
    	EC.visibility_of_element_located((By.ID, eleId))
	)

def getBillLinks():
	global driver
	ribbonbills = driver.find_elements_by_class_name("ribbonbill")
	for bill in ribbonbills:
		anchor = bill.find_element_by_tag_name('a')
		billLinks.append(anchor.get_attribute('href'))
		print("URL Acquired: %s" % (anchor.get_attribute('href')))

def getVoteCount(url):
	html = urlopen(url)
	bsObj = BeautifulSoup(html, "html.parser")

	table = bsObj.find("table",{"id":"ctl00_ContentPlaceHolder1_dlVoteMember"})

	namesHTML = table.findAll("span",{"class":"text"})
	votesHTML = table.findAll("span",{"class":"textBold"})

	names = []
	votes = []

	for name in namesHTML:
		names.append(name.getText())

	for vote in votesHTML:
		votes.append(vote.getText())

	nameVotes = dict(zip(names, votes))

	changes = bsObj.find("div",{"id":"ctl00_ContentPlaceHolder1_RollCallHistDIV"}).table
	changeRows = changes.findAll("tr")
	change = ""
	for row in changeRows:
		if row.attrs['colspan'] == "1":
			if row.td.span.getText() == "Yeas" or row.td.span.getText() == "Nays To Yeas":
				change = "Y"
			elif row.td.span.getText() == "Nays" or row.td.span.getText() == "Yeas To Nays":
				change = "N"
		elif row.attrs['colspan'] == "3":
			nameVotes[row.td.getText().strip()] = change

	time.sleep(2) # Being courteous
	return nameVotes

def returnEmptyVote(cameralType):
	try:
		conn = pymysql.connect(host='127.0.0.1', unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock', user='root', passwd=None, db='flbilltrack', charset='utf8')
		cur = conn.cursor()
		cur.execute("USE flbilltrack")
		cur.execute("SELECT lname FROM %s" % (cameralType))
		cur.connection.commit()
		congressmen = cur.fetchall()
		output = {}
		for congressman in congressmen:
			output[congressman[0]] = "none"
	finally:
		cur.close()
		conn.close()

	return output

def getBillInfo(url):
	html = urlopen(url)
	bsObj = BeautifulSoup(html, "html.parser")

	# Get the bill number/name
	heading = bsObj.find("h1", {"class":"ribbonbilldetail"}).getText()
	number = heading[:heading.index("-")-2].strip()
	name = heading[heading.index("-")+1:].strip()

	# Get the bill summary
	summary = bsObj.find("span", {"id":"lblShortTitle"}).getText()

	# Get the full text URL
	fullTextURL = "http://www.myfloridahouse.gov/" + bsObj.find("a", text=re.compile("Enrolled")).attrs['href']

	# Get the voting record
	try:
		# Get the "Vote History" table
		resultsTbl = bsObj.find("table", {"id":"ctl00_ContentPlaceHolder1_ctrlContentBox_ctrlPageContent_ctl00_dgHistory"})
		resultsTblLength = len(resultsTbl.tbody.findAll("tr"))

		# Get the heading of the last row
		lastRowHeading = resultsTbl.tbody.findAll("tr")[resultsTblLength-1].findAll("td")[0].getText().strip()

		# If the last vote was a House vote, get it and work up until a heading not called "House" is found, that's the Senate vote row, vice versa.
		if lastRowHeading == "House":
			houseResults = "http://www.myfloridahouse.gov/" + resultsTbl.tbody.findAll("tr")[resultsTblLength-1].findAll("td")[6].a.attrs["href"]
			i = resultsTblLength-1
			iRowHeading = resultsTbl.tbody.findAll("tr")[i].findAll("td")[0].getText().strip()
			while iRowHeading != "Senate" and i > 0:
				i -= 1
				iRowHeading = resultsTbl.tbody.findAll("tr")[i].findAll("td")[0].getText().strip()
			senateResults = "http://www.myfloridahouse.gov/" + resultsTbl.tbody.findAll("tr")[i].findAll("td")[6].a.attrs["href"]

		elif lastRowHeading == "Senate":
			senateResults = "http://www.myfloridahouse.gov/" + resultsTbl.tbody.findAll("tr")[resultsTblLength-1].findAll("td")[6].a.attrs["href"]
			i = resultsTblLength-1
			iRowHeading = resultsTbl.tbody.findAll("tr")[i].findAll("td")[0].getText().strip()
			while iRowHeading != "House" and i > 0:
				i -= 1
				iRowHeading = resultsTbl.tbody.findAll("tr")[i].findAll("td")[0].getText().strip()
				houseResults = "http://www.myfloridahouse.gov/" + resultsTbl.tbody.findAll("tr")[i].findAll("td")[6].a.attrs["href"]

		# Get House Votes
		houseVotes = getVoteCount(houseResults)

		# Get Senate Votes
		senateVotes = getVoteCount(senateResults)

	# If no "Vote History" table was found, return an empty set of votes
	except:
		houseVotes = returnEmptyVote("representatives")
		senateVotes = returnEmptyVote("senators")

	time.sleep(2) # Being courteous
	
	return {
		"url": url,
		"number": number,
		"name": name,
		"summary": summary,
		"fullTextURL": fullTextURL,
		"senateVotes": senateVotes,
		"houseVotes": houseVotes
	}

def saveToDB(bill):
	try: 
		conn = pymysql.connect(host='127.0.0.1', unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock', user='root', passwd=None, db='flbilltrack', charset='utf8')
		cur = conn.cursor()
		cur.execute("USE flbilltrack")

		print("Number: %r\n Name: %r\n Summary: %r\n fullTextURL: %r\n URL: %r" % (bill['number'], bill['name'], bill['summary'], bill['fullTextURL'], bill['url']))
		cur.execute("INSERT INTO bills(number,name,summary,fullTextURL,url) VALUES(%s,%s,%s,%s,%s)", (bill['number'], bill['name'], bill['summary'], bill['fullTextURL'], bill['url']))
		cur.connection.commit()

		cur.execute("SELECT id FROM bills ORDER BY ID DESC LIMIT 1")
		cur.connection.commit()
		billId = str(cur.fetchone()[0])

		for key, value in sorted(bill["houseVotes"].items()):
			cur.execute("INSERT INTO votes(cameral,congressman,billid,vote) VALUES(%s,%s,%s,%s)", ("House", key, billId,value))
			cur.connection.commit()
			print("Cameral: %s, Congressman: %s, Bill Id: %s, Vote: %s" % ("House", key, billId, value))

		for key, value in sorted(bill["senateVotes"].items()):
			print("Cameral: %s, Congressman: %s, Bill Id: %s, Vote: %s" % ("Senate", key, billId, value))
			cur.execute("INSERT INTO votes(cameral,congressman,billid,vote) VALUES(%s,%s,%s,%s)", ("Senate", key, billId,value))
			cur.connection.commit()

		cur.close()
	finally:
		conn.close()


# Program Start
billLinks = []

# Get to Enrolled Bills
driver = webdriver.Firefox()
driver.get("http://www.myfloridahouse.gov/Sections/Bills/bills.aspx")
assert "Florida" in driver.title
select = Select(driver.find_element_by_name('ddlBillList'))
select.select_by_value("1")
scrollToElement("btnShowBills")
driver.find_element_by_id("btnShowBills").click()

# Get all the pages
pageVals = [];
pageNav = driver.find_element_by_name("ddlPaging")
pageLinks = pageNav.find_elements_by_css_selector("*")
for pageLink in pageLinks:
	pageVals.append(pageLink.get_attribute('value'))

# For each page, get all the bill links
for pageVal in pageVals:
	select = Select(driver.find_element_by_name('ddlPaging'))
	select.select_by_value(pageVal)
	element = WebDriverWait(driver, 10).until(
    	EC.presence_of_element_located((By.ID, "pnlLeavingMyFloridaHouse"))
	)
	getBillLinks()
driver.close()

# For each bill, get all the info and save it to a database
for billLink in billLinks:
	saveToDB(getBillInfo(billLink))
