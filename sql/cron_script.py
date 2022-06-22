import os
import time
import datetime
import mysql.connector

connection = mysql.connector.connect(host=os.environ.get('DB_HOST', 'localhost'), user=os.environ.get('DB_USER', 'root'), password=os.environ.get('DB_PASS', ''), database=os.environ.get('DB_NAME'))
cursor = connection.cursor()
cursor.execute('UPDATE news SET archived = 1 WHERE datetime < NOW() - INTERVAL 1 MONTH')
cursor.close()
print("Cron: Archived news older than 1 month")

DATETIME = time.strftime('%m%d%Y-%H%M%S')
TODAYBACKUPPATH = "/backups/" + DATETIME
os.system(f"mysqldump --host {os.environ.get('DB_HOST', 'localhost')} -P {os.environ.get('DB_PORT', 3306)} -u {os.environ.get('DB_USER', 'root')} -p{os.environ.get('DB_PASS', '')} {os.environ.get('DB_NAME')} > {TODAYBACKUPPATH}.sql")
print("Cron: Backup database complete, file: " + TODAYBACKUPPATH + ".sql")
