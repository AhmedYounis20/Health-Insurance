from mysql import connector
database=connector.connect(host='localhost',user='team',password='team',database='insurancecompany')
from datetime import datetime


cur=database.cursor()

########## Plans DM ##################
def PlanDetails(id):
    result=[]
    try:
        cur.execute(f'select type,description,name,website,country,region,city,street,hospital.hospitalid from plan,hospitalplan,hospital where plan.planid=hospitalplan.planid and hospitalplan.hospitalid=hospital.hospitalid and plan.planid={id};')
        result+=cur.fetchall()
    except connector.Error as e:
        print("exception", e)
    return result

def planlist():
    try:
        cur.execute('select planid,type,Description from plan;')
    except connector.Error as e:
        print("exception", e)
    return(cur.fetchall())

def changePlan(customerEmail,newPlan):
    cur.execute(f"update Customer set PlanId={newPlan} where Email='{customerEmail}';")
    database.commit();

########## Hospitals DM ##################

def addhospital(name=None,website=None,country=None,region=None,city=None,street=None,Contacts=[],plans=[]):
    cur.execute(f"insert into hospital(name,website,country,region,city,street)values('{name}','{website}','{country}','{region}','{city}','{street}');")
    
    database.commit()
    cur.execute(f"select hospitalid from hospital where name='{name}'")
    hos_id=cur.fetchall()[0][0]
    for plan in plans:
        print(plan)
        cur.execute(f"insert into hospitalPlan(hospitalid, planid) values ({hos_id},{plan});") 
        database.commit()
    for i in Contacts: 
        if i != None:
            cur.execute(f"insert into hospitalcontacts(hospitalid, phone) values ({hos_id},'{i}');") 
            database.commit()

def HospitalDetails(id):
    try:
        cur.execute(f'select name,country,region,city,street,type as plan ,phone,website,plan.planid  from hospital left join hospitalplan on  hospital.hospitalid=hospitalplan.hospitalid left join plan on hospitalplan.planid =plan.planid left join hospitalcontacts on  hospital.hospitalid=hospitalcontacts.hospitalid  where hospital.hospitalid={id};')
    except connector.Error  as e:
        print('exception',e)
    return cur.fetchall()


def HospitalList():
    try :
        cur.execute('select name,Country,region,city,Street,hospitalid from hospital;')

    except connector.Error as e:
        print("Exception",e)
    return cur.fetchall()

def HospitalId(name):
    cur.execute(f"select hospitalid from hospital where name='{name}' ")  
    return cur.fetchall()[0][0]
  

def RemoveHospital(id=None):
    try:
        cur.execute(f'Delete from hospital where hospitalid={id};')
        database.commit()

    except connector.Error as e:
        print(e)


########## admin DM ##################

########## Customer DM ##################
def AddCustomer(FirstName=None,LastName=None,Age=None,Email=None,PlanId=1,Contacts=[],HolderId=0,stuff=0):


    if HolderId==0:
        cur.execute(f"insert into customer(FirstName,LastName,holderid,Email,Age,planid,RegistrationDate,stuff) values('{FirstName}','{LastName}',1,'{Email}','{Age}',{PlanId},'{str(datetime.now().strftime('%Y-%m-%d'))}','{stuff}')")
        database.commit()
        cur.execute(f"update customer set holderid=customerid where email='{Email}';")
        database.commit()
    else:
        cur.execute(f"insert into customer(FirstName,LastName,holderid,Email,Age,planid,RegistrationDate,stuff) values('{FirstName}','{LastName}',{HolderId},'{Email}','{Age}',{PlanId},'{str(datetime.now().strftime('%Y-%m-%d'))}','{stuff}')")
        database.commit()

    cur.execute(f"select customerid from customer where email='{Email}';")
    Cus_id=cur.fetchone()[0]
    print(Cus_id)

    try: 
        cur.execute(f"select customerId from customer where email='{Email}';") 
    except connector.Error as e: 
        print('Exception',e) 
    cus_id = cur.fetchone()[0]
    print(cus_id)
    for i in Contacts: 
        cur.execute(f"insert into customercontact(customerid, phone) values ({cus_id},'{i}');") 
        database.commit()


def CustomerDetails(id=None,email=None):
    try:
        if id :
            cur.execute(f"select customer.CustomerId,HolderId,FirstName,LastName,Email,type,phone,age,RegistrationDate,plan.PlanId  from customer left join customercontact on customer.customerid=customercontact.customerid left join plan on customer.planid=plan.planid where customer.customerid={id}; ")
        if email:
            cur.execute(f"select customer.CustomerId,HolderId,FirstName,LastName,Email,type,phone,age,RegistrationDate,plan.PlanId   from customer left join customercontact on customer.customerid=customercontact.customerid left join plan on customer.planid=plan.planid where customer.email='{email}'; ")

    except connector.Error as e:
        print(e)
    return cur.fetchall();    

def CustomerList(): 
    try:
        cur.execute('select * from customer ;')

    except connector.Error as e:
        print(e)
    return cur.fetchall()

def RemoveCustomer(id):
    try:
        cur.execute(f'Delete from Customer where CustomerId={id} ;')
        database.commit()

    except connector.Error as e:
        print(e)


############## Dependent DM #################

def AddDependent(holder_email, first, last, email, plan, age):

    submittingDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cus_id=CustomerDetails(email=holder_email)[0][0]
    AddCustomer( FirstName=first,LastName=last,PlanId=plan,Email=email,Age=age ,HolderId=cus_id)


def DependentList(holder_id):

    try:

        cur.execute(f"select CustomerId, FirstName, LastName, Age, RegistrationDate, Type  from customer, plan where HolderId = '{holder_id}' and customer.PlanId = plan.PlanId and CustomerId <> HolderId;")

    except connector.Error as e:

        print("exception", e)

    return cur.fetchall()





def UpdateCustomer(**kwargs):
    try:
        if kwargs['FirstName']:
            cur.execute(f"update customer set FirstName='{kwargs['FirstName']}' where Customerid ={kwargs['CustomerId']}")
        if kwargs['LastName']:
            cur.execute(f"update customer set LastName='{kwargs['LastName']}' where Customerid ={kwargs['CustomerId']}")
        if kwargs['Age']:
            cur.execute(f"update customer set {kwargs['Age']} where Customerid ={kwargs['CustomerId']}")
        if kwargs['PlanId']:
            cur.execute(f"update customer set {kwargs['PlanId']} where Customerid ={kwargs['CustomerId']}")
    except connector.Error as e :
        print(e)

def UpdateDependant(**kwargs):
    UpdateCustomer(kwargs)


##################### admin #############
def AddAdmin(FirstName=None,LastName=None,Age=None,Email=None,Facebook=None,Github=None,LinkedIn=None,imagepath=None,Contacts=[]):
    try:
        cur.execute(f"insert into admin(firstname,lastname,age,email,facebook,github,linkedin,imagepath,RegistrationDate)values('{FirstName}','{LastName}','{Age}','{Email}','{Facebook}','{Github}','{LinkedIn}','{imagepath}','{str(datetime.now().strftime('%Y-%m-%d'))}');")
        database.commit()
        AddCustomer(FirstName=FirstName,LastName=LastName,Age=Age,Email=Email,Contacts=Contacts,stuff=1,PlanId=3)
    except connector.Error as e:
        print(e)
        

def AdminList():
    try:
        cur.execute('select * from admin;')
    except connector.error as e :
        print(e)
    return cur.fetchall();


############### Claim DM ###########################
# createclaim
def CreateClaim (CustomerEmail,HospitalName,Description,Expense):
    resolved = 0
    submittingDate = datetime.now().strftime('%Y-%m-%d')
    try:
        cur.execute(f"select CustomerId from Customer where Upper(Customer.Email)=Upper('{CustomerEmail}');")
        result1= cur.fetchall()
        cur.execute(f"select HospitalId from Hospital where Upper(Hospital.Name)=Upper('{HospitalName}');")
        result2=cur.fetchall()
        # print(result1)
        # print(result2)
        CustomerId= result1[0][0]
        HospitalId = result2[0][0]
        cur.execute(f"insert into claim (HospitalId,CustomerId,resolved,SubmittingDate,Expense,Description) values ({HospitalId},{CustomerId},{resolved},'{submittingDate}',{Expense},'{Description}');")
        database.commit()
    except connector.Error as e:
        print("Exception" , e)
#ClaimDetail
def ClaimDetail(id):
    try:
        cur.execute(f'select name,country,region,city,street,customer.customerid,resolved,submittingdate,expense,description,firstname,lastname,claim.claimid from customer,claim,hospital where claimid= {id} and claim.customerid=customer.customerid and hospital.hospitalid=claim.hospitalid and claim.customerid=customer.customerid;')
    except connector.Error as e:
        print("exception", e)
    return cur.fetchall()


#customerclaims
def CustomerClaims(customer_id=None,CustomerEmail=None):
        
    try:
        if CustomerEmail:
            customer_id=CustomerDetails(email=CustomerEmail)[0][0]
        cur.execute(f"select * from claim where CustomerId = {customer_id};")
    except connector.Error as e:
        print("exception", e)
    return cur.fetchall()

def resolveClaims():
    cur.execute("select * from claim;")
    results = cur.fetchall() #[(2, 88, 0, datetime.date(2022, 1, 2), 2343, 'pl pla\r\ni am fucking khatabb!!!'), (1, 2, 0, datetime.date(2022, 1, 2), 1000, 'pla pla pla'), (4, 88, 0, datetime.date(2022, 1, 2), 9000, 'PLA PLA !!'), (2, 3, 0, datetime.date(2022, 1, 4), 1258, 'Teeth operation')]
    allCliams=[]
    for result in results :
        result=list(result)
        HospitalId=result[1]
        cur.execute(f"select Name from Hospital where HospitalId ={HospitalId};")
        fetchedName=cur.fetchone()[0]
        result[1] = fetchedName
        CustomerId=result[2]
        cur.execute(f"select Email from Customer where CustomerId ={CustomerId};")
        fetchedEmail=cur.fetchone()[0]
        result[2]=fetchedEmail

        if(result[3] == 0):
            result[3]='un resolved'
        else:
            result[3] = "resolved"
        submitingDate = result[4]
        result[4] = str(submitingDate)
        allCliams.append(result)
    print(allCliams)
    return allCliams
    
def resolveTheClaim(claimId):
    cur.execute(f"update claim set resolved = 1 where ClaimId={claimId} ;")
    database.commit()