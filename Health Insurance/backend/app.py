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


############ home Routes ###################
@app.route('/')
def first():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('layout.html')




########## Plans Routes ##################
@app.route('/plan/all')
def PlanList():
    plans=D.planlist()
    return render_template('/plan/planList.html',plans=plans)

@app.route('/plan/<id>')
def PlanDetails(id):
    records=D.PlanDetails(id)
    return render_template('/plan/planDetails.html',records=records)

@app.route('/home/changePlan' , methods=["POST","GET"])
def changePlan():
    if request.method == "GET" :
        return render_template('/customer/changePlan.html')
    else:
        CustomerEmail = request.form.get("Email")
        newPlan = request.form.get('newPlan')
        D.changePlan(CustomerEmail,newPlan)
        return redirect(url_for('home'))
############## Hospitals Routes #################
@app.route('/hospital/register',methods = ['GET','POST'])
def AddHospital():
    if request.method=='GET':
        return render_template('hospital/hospitalform.html')

    if request.method=='POST':
        
        D.addhospital(request.form.get('Name'),request.form.get('Website'),request.form.get('Country'),request.form.get('Region'),request.form.get('City'),request.form.get('Street'),request.form.getlist('Phone'),request.form.getlist('plan'))
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

############## cutomer Routes #################
@app.route('/customer/register',methods=['POST','GET'])
def AddCustomer():
    if request.method=="GET":
        return render_template('customer/customerform.html')
    else:
        D.AddCustomer(FirstName=request.form.get("FirstName"),LastName=request.form.get("LastName"),Age=request.form.get("Age"),Email=request.form.get("Email"),PlanId=request.form.get("Plan"),Contacts=request.form.getlist("Phone"))
        return redirect(f'/customer/Profile?Email={request.form.get("Email")}')

@app.route('/customer/Profile')
def CustomerProfile():
    
    customer=D.CustomerDetails(email=request.args.get('Email'))
    if len(customer) == 0:
        return render_template('layout.html',error=True)
    contacts=[i[6]  for i in customer if i[6]!=None ]
    dependants=D.DependentList(customer[0][0])
    return render_template('customer/customerProfile.html',customer=customer,contacts=contacts,dependants=dependants) 

@app.route('/customer/all')
def CustomerList():
    return render_template('customer/customerlist.html',customers=D.CustomerList())

@app.route('/customer/remove',methods=['GET','POST'])
def RemoveCustomer():
    if request.method=='GET':
        customers=D.CustomerList()
        return render_template('customer/customerRemove.html',customers=customers)
    else:
        print()
        D.RemoveCustomer(request.form.get('customer'))
        return redirect(url_for('CustomerList'))

############## Dependents Routes #################
@app.route('/customer/addDependent', methods=['POST','GET'])
def AddDependent():

    if request.method=='GET':
        return render_template('/customer/addDependant.html')
    else:

        holder_email = request.form.get('HolderEmail')
        first = request.form.get('FirstName')
        last = request.form.get('LastName')
        email = request.form.get('Email')
        plan = request.form.get('Plan')
        age = request.form.get('Age')
        D.AddDependent(holder_email, first, last, email, plan, age)
        return redirect('/')
    
@app.route('/customer/dependantlist')
def DependantList():
    return render_template('/customer/dependantList.html')

############## Claims Routes #################

@app.route('/claim/create' , methods=["POST","GET"])
def CreateClaim():
    hospitals=D.HospitalList()

    if request.method == "GET" :
        return render_template('claim/claimform.html',hospitals=hospitals)
    else:
        CustomerEmail = request.form["Email"]
        Hospital = request.form["HospitalName"]
        Hospital_id=D.HospitalId(Hospital)
        HospitalDetails=D.HospitalDetails(Hospital_id)
        CustomerDetails=D.CustomerDetails(email=CustomerEmail)
        
        error = (HospitalDetails[0][8]!=CustomerDetails[0][9])
        if error:
            return render_template('claim/claimform.html',hospitals=hospitals,error=error)
        
        Expense = request.form["Expense"]
        Description = request.form["Description"]
        D.CreateClaim (CustomerEmail,Hospital,Description ,Expense)
        return redirect(url_for('home'))

@app.route('/claim/<id>')
def ClaimDetails(id):
    records=D.ClaimDetail(id)
    return render_template('/claim/claimdetails.html',records=records)    

@app.route('/claim/all', methods=['POST','GET'])
def ClaimList():
    if request.method == 'GET':
        return render_template('/claim/claimList.html')
    else:
        CustomerEmail = request.form.get('Email')
        claims = D.CustomerClaims(CustomerEmail=CustomerEmail)
        return render_template('/claim/claimListlist.html', data=claims)

@app.route('/home/resolveClaims')
def resolveClaims():
    allclaims =D.resolveClaims()

    return render_template('/claim/resolveClaims.html' , allclaims=allclaims)

@app.route('/home/resolveClaims/<claimId>')
def resolving(claimId):
    D.resolveTheClaim(claimId)
    allclaims =D.resolveClaims()
    return render_template('/claim/resolveClaims.html' , allclaims=allclaims)

########################### main function to run flask
if __name__=='__main__':
    app.run(debug=True)