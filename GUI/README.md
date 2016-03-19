# Florida Legislature Scraper

#### Description
The Florida Legislature Scraper is a python3.x web scraper that gets the voting record of the current legislative session. Only bills that are "Enrolled" (sent to the Governor for final signature) are included. This means that the dataset acquired does not include any votes on motions that were defeated on the floor, in committee, or before then. Along with each individual vote cast, the data gathered includes the following.

##### Legislators
* Name
* District
* Party
* County

##### Bills
* Number
* Name
* Summary
* Link To Full Text
* Link To Official Page

#### Files
Included in the repo are the following files:
* **FLBillTracker:** Acquires all the bill and vote information
* **repExtractor:** Acquires info on all the sitting members of Florida's House of Representatives
* **senatorExtractor:** Acquires info on all the sitting members of Florida's Senate
* **legislatureCheck:** Used to make sure data was properly gathered (see "Error Checking" below)
* **baseDB:** The base database needed to run this scraper
* **flbilltrack:** Database with all the 2016 legislative session data (end result of running the scraper)
* **data-excel:** All the scraped information in an excel file
* **GUI:** An HTML visualization of the data [(live preview)](http://andrewbriz.com/WebApps/FlLegilatureTracker/)

#### Dependencies
* [BeautifulSoup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Selenium](http://selenium-python.readthedocs.org/)
* [PyMySQL](https://github.com/PyMySQL/PyMySQL)

#### Setup
1. Create virtual environment (optional, but highly recommended)
2. Install all dependencies
3. Set up baseDB on your database
4. Run repExtractor and senatorExtractor
5. Run FLBillTracker
6. Run legislatureCheck for error checking (optional)

#### Error Checking
This scraper does not come with a much error checking built in. It is highly recommended to double check the official URL links if you plan on publishing any of this data. One almost guaranteed error is that many names on the legislator lists don't match up with those on the vote records. For example Rep. John Cortes's last name will be saves as "Cortes" in the database, but will appear as "Cortes, J." on the voting record. To fix all of these inconsistencies, run legislatureCheck and make sure that every legislator has a vote record. Make sure to clear both the bills and votes tables and reset their AUTO_INCREMENT back to 1 before running the scraper to avoid duplication of data.