import mysql.connector

mydb= mysql.connector.connect(host='bp2l5vhn6siegz1ldmh2-mysql.services.clever-cloud.com',user='u7o4e3veisc7fz1i',passwd='aWxZSRii76R3d2yR6kIs', database='bp2l5vhn6siegz1ldmh2')
print(mydb)
mycursor=mydb.cursor()
fullname='hemant'
emailid='happy@gmail.com'
password='chaku'
mycursor.execute("INSERT INTO customerlogin (fullname, emailid, password) values ('{fullname}', '{emailid}', '{password}')")
mydb.commit()