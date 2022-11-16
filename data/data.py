import json
import mysql.connector


# Establish the connection and the cursor
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='website'
)

mycursor = mydb.cursor()

# Create table: `attractions`
sql = 'DROP TABLE IF EXISTS `attractions`'
mycursor.execute(sql)

sql = '''CREATE TABLE `attractions`(
    id bigint primary key auto_increment,
    name varchar(255) not null,
    CAT varchar(255) not null,
    MRT varchar(255),
    address varchar(255),
    file varchar(2047) not null,
    direction varchar(511),
    description varchar(2047)
)'''

mycursor.execute(sql)

# Handle with attractions' json data
with open('./data/taipei-attractions.json', mode='r', encoding='utf-8') as file:
    data = json.load(file)

dataList = data['result']['results']

# Insert records in the `attractions` table
tableAttributes = ['name', 'CAT', 'MRT', 'address', 'file', 'direction', 'description']
for attraction in dataList:
    attractionDataList = list(attraction[key] for key in tableAttributes) # Store values of tableAttributes

    # Filter NOT JPG or PNG files out
    url = attractionDataList[tableAttributes.index('file')]
    urlList = url.split('https://')
    organizedUrlList = []
    for link in urlList:
        if link.endswith('.jpg') or link.endswith('.JPG') or link.endswith('.png') or link.endswith('.PNG'):
            organizedUrlList.append('https://' + link)
    attractionDataList[tableAttributes.index('file')] = ''.join(organizedUrlList)
    
    # Insert records
    val = tuple(attractionDataList)
    sql = "INSERT INTO `attractions` (name, CAT, MRT, address, file, direction, description) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    mycursor.execute(sql, val)
    mydb.commit()

# Close the cursor and the connection
mycursor.close()

mydb.close()