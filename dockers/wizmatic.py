import mysql.connector # type: ignore
import time
import os

import scripts.imagepull as impl


# Function to establish a connection to the database
def create_connection():
    try:
        db = mysql.connector.connect(
            host="db",  # This is the service name in docker-compose.yml
            user="user",  # This should be your actual username
            password="password",  # This should be your actual password
            database="wizmatic",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        return db
    except mysql.connector.Error as err:
        print(f"Failed to connect to database: {err}")
        return None

# time.sleep(20)
# Try to connect to the database until it's ready
db = None
while db is None:
    db = create_connection()
    time.sleep(2)  # Wait for 2 seconds before trying again

cursor = db.cursor()
print('ENTER WIZMATIC')
time.sleep(1)  # Wait for 1 second before starting

print("Start Test")

#impl.pullImage(url='https://www.imagebam.com/view/MEV4DVE')

print("End Test")


# Close the cursor and connection
try:   
   cursor.close()
except:
   print('Cursor not closed because it is empty')
db.close()

print('EXIT WIZMATIC')