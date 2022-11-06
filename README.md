This project was done for the accounts department that looks after a chain of
supermarket stores. It automates the downloading of invoices from a Newspaper company's website.

Benefits: 
-It saves having to log in with a username and password for every store and then waiting for 
each page to load before downloading each invoice.
-The newspaper company's website has a glitch whereby the invoice sometimes doesn't 
download properly when click the download button. This project has been coded to take this into
account and re-downloads and deletes the invoice that downloaded with a size of 0 bytes.
-When the invoices are downloaded they are merged together into one document.

Other Benefits:
-There are other divisions within the supermarket company which use this vendor to purchase 
newspapers for their supermarkets. This code can be re-used with the relevant log ins for 
those stores.
-Also, the various divisions within the supermarket company have a second newspaper vendor. This
code can be re-used as has been broken up into functions which would be suitable.

Most functions are in newspapers.py file (general methods that can be re-used for the other newspaper vendor. 
eason.py has functions specific to this vendor. There is also the spreadsheet which has the logins (dummy info put into this). 
