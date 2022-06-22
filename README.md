# Department News Board
### Nicholas SV - C14190034

### In the root folder
Build all docker images:
```bash
make build
```
this will build all the images required and initiate the database

Run all docker containers:
```bash
docker-compose up
```
### Cron jobs
- Archiving news that one month old everyday
- Backing up sql everyday
cron-backup
```bash
0 0 * * * python3 /cron_script.py > /backups/log.txt
```
cron_script.py
```python
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
```

# User Service

## Request: Register
![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/register**</span>

```json
{
    "username": "username",
    "password": "password"
}
```

### Responses:
#### Register - Successful
![CREATED](https://badgen.net/badge/CREATED/201/green)
```json
{
    "action": "register",
    "action_status": "success",
    "register_status": "success",
    "username": "username",
    "message": "Registration successful"
}
```
#### Register - Already Registered
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "register",
    "action_status": "success",
    "register_status": "username_registered",
    "message": "Username already registered"
}
```
#### Register - Already Logged In
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "register",
    "action_status": "success",
    "register_status": "already_logged_in",
    "message": "Already logged in, please logout first before registering"
}
```
#### Register - Bad Request (Incomplete)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "register",
    "action_status": "error",
    "message": "Bad request: missing '('username', <class 'str'>)' parameter"
}
```
#### Register - Bad Request (Wrong Type)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "register",
    "action_status": "error",
    "message": "Bad request: 'username' parameter is not of type '<class 'str'>'"
}
```
#### Register - Bad Request (Non JSON)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "register",
    "action_status": "error",
    "message": "Bad request: invalid data"
}
```

<br>

## Request: Login
![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/login**</span>

```json
{
    "username": "username",
    "password": "password"
}
```

### Responses:
#### Login - Successful
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "login",
    "action_status": "success",
    "login_status": "success",
    "username": "username",
    "message": "Login successful"
}
```
#### Login - Already Logged In
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "login",
    "action_status": "success",
    "login_status": "already_logged_in",
    "message": "Already logged in, please logout first before logging back in"
}
```
#### Login - Username Not Exist
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "login",
    "action_status": "success",
    "login_status": "username_not_exist",
    "message": "Username does not exist"
}
```
#### Login - Wrong Password
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "login",
    "action_status": "success",
    "login_status": "password_not_match",
    "message": "Password does not match"
}
```
#### Login - Bad Request (Incomplete)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "login",
    "action_status": "error",
    "message": "Bad request: missing '('password', <class 'str'>)' parameter"
}
```
#### Login - Bad Request (Wrong Type)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "login",
    "action_status": "error",
    "message": "Bad request: 'username' parameter is not of type '<class 'str'>'"
}
```
#### Login - Bad Request (Non JSON)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "login",
    "action_status": "error",
    "message": "Bad request: invalid data"
}
```

<br>

## Request: Logout
![DELETE](https://badgen.net/badge/Method/DELETE/red)<span style="padding:10px">**/logout**</span>


### Responses:
#### Logout - Successful
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "logout",
    "action_status": "success",
    "message": "Logged out successfully"
}
```

<br>


# News Service

## Request: Get All News
![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/news**</span>


### Responses:
#### Get All News - Successful
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "get_all_news",
    "action_status": "success",
    "message": "News fetched successfully",
    "news": [
        {
            "id": 1,
            "title": "News1 title",
            "content": "News1 Content",
            "datetime": "2011-05-20T15:04:03",
            "publisher": "test_username_a",
            "archived": 0
        }
    ],
    "count": 1
}
```

<br>

## Request: Get News
![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/news/`<int:news_id>`**</span>


### Responses:
#### Get News - Successful
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "get_news_by_id",
    "action_status": "success",
    "message": "News fetched successfully",
    "news": {
        "id": 1,
        "title": "News1 title",
        "content": "News1 Content",
        "datetime": "2011-05-20T15:04:03",
        "publisher": "test_username_a",
        "archived": 0
    }
}
```
#### Get News - News ID Not Exist
![NOT%20FOUND](https://badgen.net/badge/NOT%20FOUND/404/red)
```json
{
    "action": "get_news_by_id",
    "action_status": "error",
    "message": "News id does not exist"
}
```

<br>

## Request: Post a New News
![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/news/post**</span>

```json
{
    "title": "NewsTitle",
    "content": "NewsContent",
    "datetime": "2022-06-22T00:00:00",
    "files": [
        {
            "file_name": "file.gif",
            "base64_data": "<base64encodedbytes>"
        }
    ]
}
```

### Responses:
#### Post a New News - Successful
![CREATED](https://badgen.net/badge/CREATED/201/green)
```json
{
    "action": "post_new_news",
    "action_status": "success",
    "message": "News posted successfully",
    "news_id": 4
}
```
#### Post a New News - Not Logged In
![UNAUTHORIZED](https://badgen.net/badge/UNAUTHORIZED/401/red)
```json
{
    "action": "post_new_news",
    "action_status": "error",
    "message": "Unauthorized: please login first"
}
```
#### Post a New News - Bad Request (Incomplete, Main)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "post_new_news",
    "action_status": "error",
    "message": "Bad request: missing '('files', <class 'list'>)' parameter"
}
```
#### Post a New News - Bad Request (Incomplete, Files)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "post_new_news",
    "action_status": "error",
    "message": "Bad request: missing '('file_name', <class 'str'>)' parameter at file index 0"
}
```
#### Post a New News - Bad Request (Wrong Type, Main)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "post_new_news",
    "action_status": "error",
    "message": "Bad request: 'title' parameter is not of type '<class 'str'>'"
}
```
#### Post a New News - Bad Request (Wrong Type, Files)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "post_new_news",
    "action_status": "error",
    "message": "Bad request: 'file_name' parameter is not of type '<class 'str'>' at file index 0"
}
```
#### Post a New News - Bad Request (Non JSON)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "post_new_news",
    "action_status": "error",
    "message": "Bad request: invalid data"
}
```

<br>

## Request: Edit News
![PUT](https://badgen.net/badge/Method/PUT/blue)<span style="padding:10px">**/news/`<int:news_id>`**</span>

```json
{
    "title": "NewsTitleEdited",
    "content": "NewsContentEdited",
    "datetime": "2022-06-22T06:09:00",
    "files": [
        {
            "file_name": "fileEdited.gif",
            "base64_data": "<base64encodedbytes>"
        }
    ]
}
```

### Responses:
#### Edit News - Successful (All)
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "edit_news",
    "action_status": "success",
    "message": "News edited successfully"
}
```
#### Edit News - Successful (Partial)
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "edit_news",
    "action_status": "success",
    "message": "News edited successfully"
}
```
#### Edit News - Not Logged In
![UNAUTHORIZED](https://badgen.net/badge/UNAUTHORIZED/401/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Unauthorized: please login first"
}
```
#### Edit News - Not the Publisher
![FORBIDDEN](https://badgen.net/badge/FORBIDDEN/403/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Forbidden: you are not the publisher of this news"
}
```
#### Edit News - News ID Not Exist
![NOT%20FOUND](https://badgen.net/badge/NOT%20FOUND/404/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "News id does not exist"
}
```
#### Edit News - Bad Request (Incomplete, Main)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Bad request: 'title' parameter is not of type '<class 'str'>'"
}
```
#### Edit News - Bad Request (Incomplete, Files)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Bad request: missing '('file_name', <class 'str'>)' parameter at file index 0"
}
```
#### Edit News - Bad Request (Wrong Type, Main)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Bad request: 'title' parameter is not of type '<class 'str'>'"
}
```
#### Edit News - Bad Request (Wrong Type, Files)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Bad request: 'file_name' parameter is not of type '<class 'str'>' at file index 0"
}
```
#### Edit News - Bad Request (Unknown Parameters, Main)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Bad request: unknown parameters: yep, why, unknown"
}
```
#### Edit News - Bad Request (Unknown Parameters, Files)
![BAD%20REQUEST](https://badgen.net/badge/BAD%20REQUEST/400/red)
```json
{
    "action": "edit_news",
    "action_status": "error",
    "message": "Bad request: unknown parameters: unknown, yep, why at file index 0"
}
```

<br>

## Request: Delete News
![DELETE](https://badgen.net/badge/Method/DELETE/red)<span style="padding:10px">**/news/`<int:news_id>`**</span>


### Responses:
#### Delete News - Successful
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "delete_news",
    "action_status": "success",
    "message": "News deleted successfully"
}
```
#### Delete News - News ID Not Exist
![NOT%20FOUND](https://badgen.net/badge/NOT%20FOUND/404/red)
```json
{
    "action": "delete_news",
    "action_status": "error",
    "message": "News id does not exist"
}
```
#### Delete News - Not Logged In
![UNAUTHORIZED](https://badgen.net/badge/UNAUTHORIZED/401/red)
```json
{
    "action": "post_new_news",
    "action_status": "error",
    "message": "Unauthorized: please login first"
}
```
#### Delete News - Not the Publisher
![FORBIDDEN](https://badgen.net/badge/FORBIDDEN/403/red)
```json
{
    "action": "delete_news",
    "action_status": "error",
    "message": "Forbidden: you are not the publisher of this news"
}
```

<br>


# File Service

## Request: Get File
![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/file/`<int:news_id>`**</span>


### Responses:
#### Get File - Successful
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "action": "get_files_from_news_id",
    "action_status": "success",
    "message": "Files fetched successfully",
    "files": [
        {
            "file_name": "file.gif",
            "base64_data": "<base64encodedbytes>"
        }
    ],
    "count": 1
}
```
#### Get File - News ID Not Exist
![NOT%20FOUND](https://badgen.net/badge/NOT%20FOUND/404/red)
```json
{
    "action": "get_files_from_news_id",
    "action_status": "error",
    "message": "News id does not exist"
}
```

<br>


