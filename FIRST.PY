from flask import Flask, render_template,request,redirect,url_for
import mysql.connector




app = Flask(__name__)
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mis"
)
cursor=db.cursor()
@app.route("/")
def HomePage():
    cursor.execute("select distinct department from personal")
    listDepartments=cursor.fetchall()
    return render_template("Homepage.html",list=listDepartments)

@app.route("/departmentEmployees/<dname>")
def departmentEmployees(dname):
    selectCountQuery= "select count(*) from personal where department='"+dname+"'"
    cursor.execute(selectCountQuery)
    deptCount=cursor.fetchone()
    selectQuery="select * from personal where department='"+dname+"'"
    cursor.execute(selectQuery)
    list=cursor.fetchall()
    return render_template("employeeslist.html",department=dname,employees=list,dcount=deptCount)


@app.route("/newemployee")
def newRecord():
    return render_template("entryform.html")

@app.route("/saverecord",methods=["POST"])
def saverecord():
    
    cursor.execute("insert into personal values("+ request.form['empno']+",'"+request.form['employeename']+"','"+request.form['employeedept']+"')")
    db.commit()
    return redirect(url_for('HomePage'))


@app.route("/deleteEmployee/<empno1>/<dname1>")
def deleteEmployee(empno1,dname1):
    cursor.execute("delete from personal where empno="+empno1)
    db.commit()
    return redirect(url_for('departmentEmployees',dname=dname1))
app.run(debug=True)
