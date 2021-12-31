from flask import Flask,redirect ,request
from flask import render_template
from mysql import connector

database=connector.connect(host='localhost',
                    user='root',
                    password='raghad25',
                    database='insurancecompany')
mycurs=database.cursor()
app=Flask(__name__,template_folder='../templates',static_folder='../statics')




@app.route('/home')
def home():
    return render_template('layout.html')
@app.route('/admin')
def admin():
    return '''str(db.hospital.query())'''
@app.route('/customer/register')
def AddCustomer():
    if request.method=="GET":
        return render_template('customer/customerform.html')
@app.route('/customer/all')
def customerList():
    return 'customerlist'
# app.route('/customer/<name>-<id>/dependant/add')
# def AddDependant(name,id):
#     if request.method=="GET":
#         return render_template("customer/dependantform.html")
# app.route('/customer/<name>-<id>/dependant/all')
# def AddDependant(name,id):
#     if request.method=="GET":
#         return render_template("customer/dependants.html")

@app.route('/hospital/register')
def AddHospital():
    if request.method=='GET':
        return render_template('hospital/hospitalform.html')
@app.route('/hospital/all')
def HospitalList():
    mycurs.execute('select * from hospital;')
    hospitals=mycurs.fetchall()
    print(hospitals[0][1])
    return render_template('hospital/hospitallist.html',hospitals=hospitals)

@app.route('/claim/create')
def CreateClaim():

    return render_template('claim/claimform.html')
if __name__=='__main__':
    app.run()