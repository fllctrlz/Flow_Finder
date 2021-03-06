'''
Author: CTRL-Z Robotics

This program will read the data from the arduino program using serial ports.
It will then upload each persons data to the MySql database

'''
import serial
import MySQLdb

#connect to the database
conn = MySQLdb.connect(host= "localhost", user= "main", passwd= "ctrlzfll", db= "flowFinder")
cursor = conn.cursor()

ser = serial.Serial('/dev/ttyACM0', 9600)

prevId = -1
totalWaterUsed = 0
#this while loop will set up the MySql databse and enter each persons water consumption
while True:
    line = ser.readline().decode("utf-8").split()
    currId = int(line[0])
    amount = int(line[1])

    
    if currId > -1 and currId == prevId:
        totalWaterUsed+=amount
    
    if currId == -1 and prevId > -1:
        id = prevId

        #putting the total water usage into litres instead of ml
        litres = totalWaterUsed/1000.0

        try:
            cursor.execute("""insert into showerData (id, litres) values(%s, %s)""",(id, litres))
            conn.commit()
        except:
            conn.rollback()
        #write to database
        totalWaterUsed = 0
    
    prevId = currId
