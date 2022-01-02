from flask import Flask,redirect ,url_for,request
from flask import render_template
from mysql import connector
import DMF as D
database=connector.connect(host='localhost',
                    user='root',
                    password='raghad25',
                    database='insurancecompany')
mycurs=database.cursor()
app=Flask(__name__,template_folder='../templates',static_folder='../statics')

app.debug = True



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

@app.route('/')
def first():
    return redirect('/home')
@app.route('/hospital/register',methods = ['GET','POST'])
def AddHospital():
    if request.method=='GET':
        return render_template('hospital/hospitalform.html')

    if request.method=='POST':
        
        D.addhospital(request.form.get('Name'),request.form.get('Website'),request.form.get('Country'),request.form.get('Region'),request.form.get('City'),request.form.get('Street'),[request.form.get('Region')],request.form.getlist('plan'))
        hos_id=D.HospitalId(request.form.get('Name'))

        return redirect(url_for('HospitalDetails',id=hos_id))



@app.route('/hospital/<id>')
def HospitalDetails(id):
    hospital_records=D.HospitalDetails(id)
    hospital_plans=[]
    for i in hospital_records:
        if i[5] not in hospital_plans:
            hospital_plans+=[i[5]]
    hospital_contacts=[]
    for i in hospital_records:
        if i[6] not in hospital_contacts:
            hospital_contacts+=[i[6]]
    return render_template('hospital/hospitalDetails.html',hospital_records=hospital_records,hospital_plans=hospital_plans,hospital_contacts=hospital_contacts)

@app.route('/hospital/all')
def HospitalList():

    hospitals=D.HospitalList()
    return render_template('hospital/hospitallist.html',hospitals=hospitals)


@app.route('/hospital/remove/',methods=['POST','GET'])
def RemoveHospital():
    if request.method=='GET':
        hospitals=D.HospitalList()
        return render_template('hospital/hospitalremove.html',hospitals=hospitals)
    else:
        print(request.form.get('hospital'))
        D.RemoveHospital(request.form.get('hospital'))
        return redirect(url_for('HospitalList'))


@app.route('/claim/create')
def CreateClaim():
    return render_template('claim/claimform.html')

@app.route('/claim/all')
def ClaimList():
    return render_template('/claim/claimList.html')
@app.route('/customer/dependantlist')
def DependantList():
    return render_template('/customer/dependantList.html')
@app.route('/customer/adddependant')

def AddDependant():
    return render_template('/customer/addDependant.html')


@app.route('/plan/all')
def PlanList():
    plans=D.planlist()
    return render_template('/plan/planList.html',plans=plans)

@app.route('/plan/<id>')
def PlanDetails(id):
    records=D.PlanDetails(id)
    return render_template('/plan/planDetails.html',records=records)

if __name__=='__main__':
    app.run(debug=True)