from flask import Flask, render_template, url_for, flash, request, redirect
import db
from datetime import datetime

app = Flask(__name__)
app.config["MYSQL_USER"] = "arunachalam"
app.config["MYSQL_PASSWORD"] = "Mypassword@123"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_DB"] = "employee"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"



@app.route("/")
def home():
    conn = db.establish_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM employee_bio"
    cursor.execute(query=query)
    res = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("index.html", data=res)

@app.route("/addEmp", methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        conn = db.establish_connection()
        cursor = conn.cursor()
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        sex = request.form.get('sex')
        dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').strftime('%d-%m-%Y')
        doj = datetime.strptime(request.form.get('doj'), '%Y-%m-%d').strftime('%d-%m-%Y')
        print("DOB: ", dob)
        print("DOJ: ", doj)
        email = request.form.get('email')
        nation = request.form.get('nation')
        data = (f_name, l_name, sex, dob, doj, email, nation)
        query = f"""
            INSERT INTO employee_bio (f_name, l_name, sex, dob, doj, email, nation) 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');
        """ % data
        print("Query: ", query)
        cursor.execute(query=query)
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template("add_employee.html")

@app.route("/updateEmp/<string:emp_id>/", methods=['GET', 'POST'])
def update_employee(emp_id):
    conn = db.establish_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        query = f"SELECT * FROM employee_bio WHERE id={emp_id}"
        cursor.execute(query=query)
        res = cursor.fetchone()
        conn.commit()
        conn.close()
        return render_template("edit_employee.html", data=res)
    elif request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        sex = request.form.get('sex')
        dob = request.form.get('dob')
        doj = request.form.get('doj')
        email = request.form.get('email')
        nation = request.form.get('nation')
        data = (f_name, l_name, sex, dob, doj, email, nation)
        query = f"""UPDATE employee_bio 
            SET f_name='%s', l_name='%s', sex='%s', dob='%s', doj='%s', email='%s', nation='%s'
            WHERE id={emp_id};""" % data
        cursor.execute(query)
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

@app.route("/delEmp/<string:emp_id>/", methods=['GET'])
def del_employee(emp_id):
    if request.method == 'GET':
        conn = db.establish_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM employee_bio WHERE id={emp_id};"
        cursor.execute(query)
        conn.commit()
        conn.close()

    return redirect(url_for('home'))






if __name__ == "__main__":
    app.run(debug=True)