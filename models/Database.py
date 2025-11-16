
from config import Config
import mysql.connector
from mysql.connector import Error


def get_db_connection():
    # tạo kết nối
    try:
        conn = mysql.connector.connect(
            host= Config.MYSQL_HOST,
            user = Config.MYSQL_USER,
            passwd = Config.MYSQL_PASSWORD,
            database = Config.MYSQL_DB 
        )
        if conn.is_connected():
            print('kết nối thành công')
        else:
            print('lỗi kết nối')

        return conn
    
    except Error as e:
        print('lỗi kết nối :' + e)
        return None


def execute_query(query):
    conn = get_db_connection()
    cursor= conn.cursor(dictionary=True) # record được trả về ở dạng dict , còn reslut vẫn là một tuple [các dict ]
    
    try:

        cursor.execute(query)
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            # insert  , update , delete
            conn.commit()
            result = cursor.rowcount

        return result
    
    except Exception as e:

        print(f"Database error: {e}")
        raise e
    finally:
        
        cursor.close()
        conn.close()



