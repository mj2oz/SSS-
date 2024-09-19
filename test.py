# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'mj'
app.config['MYSQL_PASSWORD'] = '1'
app.config['MYSQL_DB'] = 'ifsb'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT FirstName, LastName FROM Employee LIMIT 5")
    employees = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee (FirstName, LastName) VALUES (%s, %s)", (first_name, last_name))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add_employee.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
