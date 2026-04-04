import pyodbc

class InvalidNameError(Exception):
    pass
def connect():
    return pyodbc.connect('driver={ODBC Driver 18 for SQL Server};Server=cypress.csil.sfu.ca;database=zjl3354;Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes')


def login(cursor, uid):
    '''
    Query if user has a valid user_id. Returns (user_id, name tuple) or None.
    '''
    cursor.execute('SELECT user_id, name FROM user_yelp WHERE user_id = ?', [uid])
    row = cursor.fetchone()
    if row:
        return row[0], row[1]
    else:
        return None, None
    
def search_business(cursor, name, city, stars, order_by):
    '''
    Query all businesses matching the given criteria. Returns list of businesses or None.
    '''
    if order_by not in ['name', 'city', 'stars']:
        raise InvalidNameError()
    query = ('SELECT business_id, name, address, city, stars FROM business '
             'WHERE stars >= ? AND name LIKE ? AND city LIKE ? '
             f'ORDER BY {order_by}')
    values = [stars, f'%{name}%', f'%{city}%']
    cursor.execute(query, values)

    row = cursor.fetchall()
    if not row:
        return None
    else:
        return row

def search_user(cursor, name, review_count, stars):
    '''
    Query all users matching the given criteria. Returns list of users or None.
    '''
    query = ('SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since FROM user_yelp '
             'WHERE average_stars >= ? AND name LIKE ? AND review_count >= ? '
             f'ORDER BY name')
    values = [stars, f'%{name}%', review_count]
    cursor.execute(query, values)

    row = cursor.fetchall()
    if not row:
        return None
    else:
        return row