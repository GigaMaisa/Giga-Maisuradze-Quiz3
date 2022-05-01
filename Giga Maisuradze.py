import sqlite3
import requests
import json

# Formula 1 Ergast API - https://www.postman.com/maintenance-astronomer-29796265/workspace/f1-api/documentation/19328871-63c4a82c-ae84-4a24-a58b-bd8a408b1c4e

# დავალება 1
year = int(input("შეიტანეთ სასურველი წელი(2014დან): "))
resp = requests.get(f'http://ergast.com/api/f1/{year}/drivers.json')
print(resp)
print(resp.status_code)
print(resp.headers)
print(resp.text)
print(resp.json())

# დავალება 2
result = resp.json()
structured_res = json.dumps(result, indent=4)
print(structured_res)
with open("data.json", 'w') as data_file:
    json.dump(result, data_file, indent=4)

# დავალება 3
user_driver = str(input('შეიყვანეთ სასურველი პილოტის გვარი: ')).capitalize()

with open('data.json') as data_file:
    res = json.load(data_file)

drivers = res['MRData']['DriverTable']['Drivers']


drivers_list = []

for driver in drivers:
    drivers_list.append(tuple(driver.values()))

print(drivers_list)






def find_driver(driver_last_name):
    driver_last_name = user_driver
    for driver in drivers:
        if driver['familyName'] == driver_last_name:
            print(json.dumps(driver, indent=4))


find_driver(user_driver)

# დავალება 4
conn = sqlite3.connect('2019_drivers_list.sqlite')
cursor = conn.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS drivers
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                driverId varchar(50),
                permanentNumber INTEGER,
                code varchar(4),
                url varchar(150),
                givenName varchar(50),
                familyName varchar(50),
                dateOfBirth varchar(10),
                nationality varchar(30)
               )
               ''')

cursor.executemany("INSERT INTO drivers (driverId, permanentNumber, code, url, givenName, familyName, dateOfBirth, nationality) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", drivers_list)


conn.commit()
conn.close()
