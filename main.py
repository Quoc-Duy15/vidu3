from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)
sqldbname = 'MyDatabase.db'

@app.route('/', methods=['GET'])
def index():
    return '11227126_Nguyen Quoc Duy'

@app.route('/emloyee', methods=['GET'])
def employee():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Employee')
    result = cur.fetchall()
    conn.close()
    return jsonify(result)

@app.route('/employee/<id>', methods=['delete'])
def delete_employee(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('DELETE FROM Employee WHERE EmployeeId = ?', (id,))
    conn.commit()
    if cur.rowcount > 0:
        return jsonify({'mesage': 'employee is deleted successfully'})
    else:
        return jsonify({'mesage': 'employee is not deleted successfully'})



@app.route('/employee', methods=['POST'])
def add_employee():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    EmployeeName = request.json.get('EmployeeName')
    AccountName = request.json.get('AccountName')
    EmployeeEmail = request.json.get('EmployeeEmail')
    Password = request.json.get('Password')
    Tel=request.json.get('Tel')
    Department = request.json.get('Department')
    Role = request.json.get('Role')
    if EmployeeName and EmployeeEmail and AccountName and Password and Tel and Department and Role:
        cur.execute(
            'insert into Employee (EmployeeName,AccountName,EmployeeEmail,Password,Tel,DepartmentID,RoleID) values (?,?,?,?,?,?,?)',
            (EmployeeName, AccountName, EmployeeEmail, Password, Tel, Department, Role)
        )
        conn.commit()
        return jsonify({'mesage': 'employee is added successfully'})


@app.route('/employee/<id>', methods=['GET','PUT'])
def update_employee(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    EmployeeName = request.json.get('EmployeeName')
    AccountName = request.json.get('AccountName')
    EmployeeEmail = request.json.get('EmployeeEmail')
    Password = request.json.get('Password')
    Tel = request.json.get('Tel')
    Department = request.json.get('Department')
    Role = request.json.get('Role')
    if EmployeeName and EmployeeEmail and AccountName and Password and Tel and Department and Role:
        cur.execute(
            'insert into Employee (EmployeeName,AccountName,EmployeeEmail,Password,Tel,DepartmentID,RoleID) values (?,?,?,?,?,?,?)',
            (EmployeeName, AccountName, EmployeeEmail, Password, Tel, Department, Role)
        )
        conn.commit()
        if cur.rowcount > 0:
            return jsonify({'message': 'Employee updated successfully'})
        else:
            return 'Employee not found', 404
    else:
        return 'EmployeeName, EmployeeEmail, Password, Tel, TotalEmployee are required', 40


@app.route('/check', methods=['POST'])
def check_EmailAddress_and_Password(EmployeeEmail, Password):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    EmployeeEmail = request.json.get('EmployeeEmail')
    Password = request.json.get('Password')
    cur.execute('SELECT * FROM Employee WHERE EmployeeEmail = ? Password = ? ', (EmployeeEmail,Password))
    employee=cur.fetchall()
    if employee:
        return jsonify({'mesage': 'employee is existed successfully'})
    else:
        return jsonify({'mesage': 'employee is not existed successfully'})


@app.route('/search',methods=['GET'])
def search_Employee():
    search = request.json.get('search')
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Employee WHERE EmployeeName like'%" + search + "%' or AccountName like'%" + search + "%' or EmployeeEmail like'%" + search + "%'")
    result = cur.fetchall()
    conn.close()
    return result

@app.route('/search_order<id>',methods=['GET'])
def search_order(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('select * from shopping where EmployeeID=?', (id,))
    result = cur.fetchall()
    return jsonify(result)


@app.route('/importEmployee',methods=['POST'])
def importEmployee():
    conn = sqlite3.connect(sqldbname)
    data = request.get_json()
    cur = conn.cursor()
    for employee in data['employees']:
        EmployeeName = employee['EmployeeName']
        AccountName = employee['AccountName']
        EmployeeEmail = employee['EmployeeEmail']
        Password = employee['Password']
        Tel = employee['Tel']
        Department = employee['Department']
        Role = employee['Role']
        cur.execute(
            'insert into Employee (EmployeeName,AccountName,EmployeeEmail,Password,Tel,DepartmentID,RoleID) values (?,?,?,?,?,?,?)',
            (EmployeeName, AccountName, EmployeeEmail, Password, Tel, Department, Role)
        )
        conn.commit()
        return jsonify({'mesage': 'employee is added successfully'})

if __name__ == '__main__':
    app.run(debug=True,port=5001)