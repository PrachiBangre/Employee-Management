from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MyDB_SQL1@Python'
app.config['MYSQL_DB'] = 'EmployeeDB'

mysql = MySQL(app)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# View all employees
@app.route('/employees')
def employees():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    cursor.close()
    return render_template('employees.html', employees=data)

# Add a new employee
@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO employees (first_name, last_name, email, phone, department) "
            "VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, email, phone, department)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('employees'))
    
    return render_template('add_employee.html')

# Edit an existing employee
@app.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
    employee = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE employees SET first_name = %s, last_name = %s, email = %s, phone = %s, "
            "department = %s WHERE id = %s",
            (first_name, last_name, email, phone, department, id)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('employees'))

    return render_template('edit_employee.html', employee=employee)

# Delete an employee
@app.route('/employee/delete/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('employees'))

    return render_template('delete_employee.html', id=id)

if __name__ == "__main__":
    app.run(debug=True)














