from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling
import os


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def get_all_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = f"""SELECT * FROM news WHERE archived = 0"""
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_news_by_id(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = f"""SELECT * FROM news WHERE id = {news_id}"""
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def add_new_news(self, title, content, datetime, publisher):
        cursor = self.connection.cursor(dictionary=True)
        sql = f"""INSERT INTO news (title, content, datetime, publisher) VALUES ('{title}', '{content}', '{datetime}', '{publisher}')"""
        cursor.execute(sql)
        self.connection.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
        

    def update_news(self, news_id, title, content, datetime):
        cursor = self.connection.cursor(dictionary=True)
        editable_fields = []
        if title:
            editable_fields.append(f"title = '{title}'")
        if content:
            editable_fields.append(f"content = '{content}'")
        if datetime:
            editable_fields.append(f"datetime = '{datetime}'")

        sql = f"""UPDATE news SET {",".join(editable_fields)} WHERE id = {news_id}"""
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def delete_news(self, news_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = f"DELETE FROM news WHERE id = {news_id}"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()


class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="news_pool",
                pool_size=32,
                pool_reset_session=True,
                host=os.environ.get('DB_HOST', 'localhost'),
                port=os.environ.get('DB_PORT', 3306),
                database=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASS', '')
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
