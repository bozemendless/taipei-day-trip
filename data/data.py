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
    category varchar(255) not null,
    description varchar(2047),
    address varchar(255),
    transport varchar(511),
    mrt varchar(255),
    lat decimal(10,8),
    lng decimal(11,8),
    images varchar(2047) not null
)'''

mycursor.execute(sql)

# Handle with attractions' json data
with open('./data/taipei-attractions.json', mode='r', encoding='utf-8') as file:
    data = json.load(file)

dataList = data['result']['results']

# Insert records in the `attractions` table
tableAttributes = ['name', 'CAT', 'description', 'address', 'direction', 'MRT', 'latitude', 'longitude', 'file']
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
    sql = "INSERT INTO `attractions` (name, category, description, address, transport, mrt, lat, lng, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    mycursor.execute(sql, val)
    mydb.commit()

# Close the cursor and the connection
mycursor.close()

mydb.close()