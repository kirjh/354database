import pyodbc
import string
import random

class InvalidNameError(Exception):
    pass

COUNTING_METHOD = 1 # 1 for review_count, 2 for actual count

def connect():
    return pyodbc.connect('driver={ODBC Driver 18 for SQL Server};Server=cypress.csil.sfu.ca;database=zjl3354;Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes')

def login(conn, uid):
    '''
    Query if user has a valid user_id. Returns user tuple or None.
    '''
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, name FROM user_yelp WHERE user_id = ?', [uid])
        row = cursor.fetchone()
        conn.commit()
        if row:
            return row
        else:
            return None, None
    except Exception as e:
        conn.rollback()
        raise e
    
def search_business(conn, name, city, stars, order_by):
    '''
    Query all businesses matching the given criteria. Returns list of businesses or None.
    '''
    try:
        cursor = conn.cursor()
        if order_by not in ['name', 'city', 'stars']:
            raise InvalidNameError()
        query = ('SELECT business_id, name, address, city, stars FROM business '
                'WHERE stars >= ? AND name LIKE ? AND city LIKE ? '
                f'ORDER BY {order_by}')
        values = [stars, f'%{name}%', f'%{city}%']
        cursor.execute(query, values)

        row = cursor.fetchall()
        conn.commit()
        if not row:
            return None
        else:
            return row
    except Exception as e:
        conn.rollback()
        raise e

def search_user(conn, name, review_count, stars):
    '''
    Query all users matching the given criteria. Returns list of users or None.
    '''
    try:
        cursor = conn.cursor()
        query = ('SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since FROM user_yelp '
                'WHERE average_stars >= ? AND name LIKE ? AND review_count >= ? '
                f'ORDER BY name')
        values = [stars, f'%{name}%', review_count]
        cursor.execute(query, values)

        row = cursor.fetchall()
        conn.commit()
        if not row:
            return None
        else:
            return row
    except Exception as e:
        conn.rollback()
        raise e
    
def make_friend(conn, user_id, friend_id):
    '''
    Insert friendship into friendship table.
    '''
    try:
        cursor = conn.cursor()
        query = ('INSERT INTO friendship(user_id, friend) VALUES(?,?)')
        values = [user_id, friend_id]
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    return

def _generate_id(length):
    id = ""
    char_list = string.ascii_letters + string.digits + "_-"
    for i in range(length):
        id += random.choice(char_list)
    return id

def review_business(conn, user_id, business_id, stars):
    '''
    Insert review into review table.
    '''
    try:
        cursor = conn.cursor()
        # Generate unique id for review_id
        review_id = None
        while True:
            review_id = _generate_id(22)
            query = ('SELECT * FROM review WHERE review_id = ?')
            cursor.execute(query, review_id)
            if not cursor.fetchone():
                break
        print(1)
        # Insert review
        query = ('INSERT INTO review(review_id, user_id, business_id, stars) VALUES(?,?,?,?)')
        values = [review_id, user_id, business_id, stars]
        cursor.execute(query, values)
        print(2)
        # Update business table
        if COUNTING_METHOD == 1:
            query = ('UPDATE business SET review_count = review_count + 1, stars = T.stars '
                     'FROM (SELECT AVG(CAST(R.stars AS DECIMAL(2, 1))) AS stars FROM review R WHERE R.business_id = ?) T '
                     'WHERE business_id = ?')
        else:
            query = ('UPDATE business SET review_count = T.count, stars = T.stars '
                     'FROM (SELECT COUNT(*) AS count, AVG(CAST(R.stars AS DECIMAL(2, 1))) AS stars FROM review R WHERE R.business_id = ?) T '
                     'WHERE business_id = ?')
        print(query)
        values = [business_id, business_id]
        cursor.execute(query, values)
        print(3)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    return