from flask import Flask, render_template, request
import sqlite3

from werkzeug.utils import redirect

connection=sqlite3.connect("Hospital.db",check_same_thread=False)
table = connection.execute("select name from sqlite_master where type='table' and name='patient'").fetchall()

if table!=[]:
    print("table already created")
else:
    connection.execute('''create table patient(
                                ID integer primary key autoincrement,
                                name text,
                                mobilenumber integer,
                                age integer,
                                address text,
                                dob text,
                                place text,
                                pincode integer                                                         
                                )''')
    print("table created successfully")

app=Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def admin_login():
    if request.method == "POST":
        getUsername=request.form["username"]
        getPassword=request.form["password"]
        print(getUsername)
        print(getPassword)
        if getUsername=="admin" and getPassword=="12345":
            return redirect("/dashboard")
    return render_template("admin.html")

@app.route("/dashboard",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        getName=request.form["name"]
        getMobilenumber=request.form["mobilenumber"]
        getAge=request.form["age"]
        getAddress=request.form["address"]
        getDob=request.form["dob"]
        getPlace=request.form["place"]
        getPincode=request.form["pincode"]
        print(getName)
        print(getMobilenumber)
        print(getAge)
        print(getAddress)
        print(getDob)
        print(getPlace)
        print(getPincode)

        try:
            query=("insert into patient(name,mobilenumber,age,address,dob,place,pincode)\
                               values('" + getName + "'," + getMobilenumber + "," + getAge + ",'" + getAddress + "','" + getDob + "','" + getPlace + "'," + getPincode + ")")
            print(query)
            connection.execute(query)

            connection.commit()
            print("inserted successfully")
        except Exception as e:
            print("Error occured ", e)

    return render_template("dashboard.html")

@app.route("/viewall")
def view():
    cursor=connection.cursor()
    count=cursor.execute("select * from patient")
    result=cursor.fetchall()
    return render_template("viewall.html",patient=result)

@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "POST":
        getMobilenumber=request.form["mobilenumber"]
        print(getMobilenumber)
        cursor = connection.cursor()
        count = cursor.execute("select * from patient where mobilenumber="+getMobilenumber)
        result = cursor.fetchall()
        return render_template("search.html", searchpatient=result)

    return render_template("search.html")

@app.route("/delete",methods = ["GET","POST"])
def delete():
    if request.method == "POST":
        getMobilenumber = request.form["mobilenumber"]
        print(getMobilenumber)


        try:
            connection.execute("delete from patient where mobilenumber=" + getMobilenumber)
            connection.commit()
            print("deleted successfully")
        except Exception as e:
            print("Error occured ", e)

    return render_template("delete.html")

@app.route("/update",methods = ["GET","POST"])
def update_patient():
    if request.method == "POST":
        mobilenumber=request.form["mobilenumber"]
        name = request.form["name"]
        age = request.form["age"]
        address = request.form["address"]
        dob = request.form["dob"]
        place = request.form["place"]
        pincode = request.form["pincode"]
        try:
            query="update patient set name='"+name+"',age="+age+",address='"+address+"',dob='"+dob+"',place='"+place+"',pincode="+pincode+" where mobilenumber="+mobilenumber
            print(query)
            connection.execute(query)
            connection.commit()
            print("Updated Successfully")
            return redirect("/viewall")
        except Exception as e:
            print(e)

    return render_template("update.html")

@app.route("/updatesearch",methods = ["GET","POST"])
def update_and_search():
    if request.method == "POST":
        getMobilenumber=request.form["mobilenumber"]
        print(getMobilenumber)
        cursor = connection.cursor()
        count = cursor.execute("select * from patient where mobilenumber="+getMobilenumber)
        result = cursor.fetchall()
        print(len(result))
        return render_template("update.html", searchpatient=result)

    return render_template("update.html")


if __name__=="__main__":
    app.run()