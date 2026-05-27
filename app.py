import flask as fl
import python.sqlserver as sql
import json

app = fl.Flask(__name__)
conn = sql.connect()

def test_credentials(conn, user_id = None):
    '''
    Get user data from user_id.
    '''
    if not user_id:
        user_id = fl.request.cookies.get('user_id')
    if not user_id:
        return (None,)
    else:
        return sql.login(conn, user_id)
    
def convert_to_list(rows):
    '''
    Convert tuples to array of comma separated strings.
    '''
    arr = []
    if not rows:
        return arr
    for row in rows:
        arr.append(",".join(map(str,row)))
    return arr

# landing page
@app.route("/")
def index():
    user_data = test_credentials(conn)
    if user_data[0]:
        return fl.redirect(fl.url_for("home"))
    else:
        return fl.render_template('login.html')

# login request, if successful loads home page
@app.route("/login", methods=['POST', 'GET'])
def login():
    if fl.request.method == 'POST':
        user_data = test_credentials(conn, fl.request.form['user_id'])
        if user_data[0]:
            response = fl.make_response(fl.redirect(fl.url_for("home")))
            response.set_cookie('user_id', user_data[0])
            return response
        else:
            error = "Incorrect user ID."
            return fl.render_template('login.html', error=error)
    return fl.redirect(fl.url_for("index"))

# log out
@app.route("/logout")
def logout():
    if fl.request.cookies.get('user_id'):
        response = fl.make_response(fl.redirect(fl.url_for("index")))
        response.delete_cookie('user_id')
        return response
    else:
        return fl.redirect(fl.url_for("index"))

# home page for logged in users
@app.route("/home", methods=['POST', 'GET'])
def home():
    user_data = test_credentials(conn)
    if user_data[0]:
        return fl.render_template('home.html', name=user_data[1])
    else:
        return fl.redirect(fl.url_for("index"))
    
# Execute search query
@app.route("/query", methods=['POST'])
def query():
    user_data = test_credentials(conn)
    if not user_data[0]:
        return fl.redirect(fl.url_for("index"))
    
    form = fl.request.form
    print(form)
    match form["query_type"]:
        case "user-search":
            try:
                rows = sql.search_user(conn, form["u_name"], form["u_review_count"], form["u_stars"])
                return convert_to_list(rows)
            except:
                return "-1"
        case "business-search":
            try:
                rows = sql.search_business(conn, form["b_name"], form["b_city"], form["b_stars"], form["b_sort_by"])
                return convert_to_list(rows)
            except:
                return "-1"

        case _:
            return "-1"

# Execute search query
@app.route("/insert", methods=['POST'])
def insert():
    user_data = test_credentials(conn)
    if not user_data[0]:
        return fl.redirect(fl.url_for("index"))
    form = fl.request.form
    print(form)
    match form["query_type"]:
        case "add-friend":
            try:
                sql.make_friend(conn, user_data[0], form["f_id"])
                return '{"msg": "Successfully added friend."}'
            except Exception as e:
                print(e)
                if e.args[0] == "23000":
                    return '{"msg": "Friendship already exists."}'
                else:
                    return '{"msg": "There was an error in your request."}'
        case "add-review":
            try:
                sql.review_business(conn, user_data[0], form["r_id"], form["r_stars"])
                return '{"msg": "Successfully left review."}'
            except Exception as e:
                print(e)
                return '{"msg": "There was an error in your request."}'
        case _:
            return "Invalid request."
    

    
