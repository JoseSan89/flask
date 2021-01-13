from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt




# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test2'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/index.html')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashpass = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (name, email, password) VALUES (%s,%s,%s)", (name, email, hashpass))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    if session['id']:
        return render_template('edit-contact.html', contact = data[0])
    else:
        return redirect(url_for('login'))

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hashpass = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuario SET name = %s, email = %s, password = %s WHERE id = %s """, (name, email, hashpass, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuario WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('login'))
        
@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM usuario WHERE name = '{0}'".format(name))
        user = curl.fetchone()
        curl.close()
        if  user != None :
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                session['id'] = user['id']
                return redirect(url_for('Index'))
            else:
                flash
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")  
        
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
