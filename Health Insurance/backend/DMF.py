from mysql import connector
database=connector.connect(host='localhost',user='team',password='team',database='insurancecompany')
from datetime import datetime


cur=database.cursor()



def HospitalList():
    try :
        cur.execute('select name,Country,region,city,Street from hospital;')

    except connector.Error as e:
        print("Exception",e)
    return cur.fetchall()
    exit

def addhospital(name=None,website=None,country=None,region=None,city=None,street=None,phone=None):
    cur.execute(f"insert into hospital(name,website,country,region,city,street)values({name},{website},{country},{region},{city},{street});")
    
    database.commit()
    cur.execute(f'insert into hospitalcontacts(phone)values({phone});')
    database.commit()
def HospitalDetails(id):
    try:
        cur.execute(f'select name,country,region,city,street,type as plan ,phone from hospital,hospitalplan,plan,hospitalcontacts where hospital.hospitalid=hospitalplan.hospitalid and hospital.hospitalid=hospitalcontacts.hospitalid and plan.planid=hospitalplan.planid and hospital.hospitalid={id};')
    except connector.Error  as e:
        print('exception',e)
    return cur.fetchall()

def RemoveHospital(id=None):
    try:
        cur.execute(f'Delete from hospital where id={id};')

    except connector.Error as e:
        print(e)


def UpdateCustomer(**kwargs):
    try:
        if kwargs['FirstName']:
            cur.execute(f"update customer set {kwargs['FirstName']} where Customerid ={kwargs['CustomerId']}")
        if kwargs['LastName']:
            cur.execute(f"update customer set {kwargs['LastName']} where Customerid ={kwargs['CustomerId']}")
        if kwargs['Age']:
            cur.execute(f"update customer set {kwargs['Age']} where Customerid ={kwargs['CustomerId']}")
        if kwargs['PlanId']:
            cur.execute(f"update customer set {kwargs['PlanId']} where Customerid ={kwargs['CustomerId']}")
    except connector.Error as e :
        print(e)
def RemoveCustomer(id):
    try:
        cur.execute(f'Delete from Customer where id={id};')

    except connector.Error as e:
        print(e)
def UpdateDependant(**kwargs):
    UpdateCustomer(kwargs)


def CutomerList():
    try:
        cur.execute('select * from customer;')

    except connector.Error as e:
        print(e)
    return cur.fetchall()

def AddCustomer(LastName=None,Age=None,Email=None,HolderId=None,PlanId=None,Contacts=[]):


    cur.execute(f"insert into customer(lastName,holderid,Email,Age,planid) values('{LastName}',{HolderId},'{Email}',{Age},{PlanId})")
    database.commit()
    cur.execute(f"update customer set holderid=customerid where email='{Email}';")
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



def AddDependent (hold_id, plan, first, last, email, age, date, admin, contact): 
    try: 
        cur.execute(f"insert into customer(holderId, planId, FirstName, LastName, Email, Age, RegistrationDate, Stuff) values ('{hold_id}','{plan}','{first}','{last}','{email}','{age}','{date}','{admin}');") 
    except connector.Error as e: 
        print('Exception',e) 
    database.commit(); 



# createclaim
def CreateClaim (customerId , HospitalId , expenses , description):
    approved = False
    submittingDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cur.execute(f"insert into claim (HospitalId,CustomerId,Approved,SubmittingDate,Expense,Description) values ({HospitalId},{customerId},{approved},{submittingDate},{expenses},{description});")
        cur.commit()
    except connector.Error as e:
        print("Exception" , e)

# adminlistclaim
def AdminListClaim () :
    try:
        cur.execute("select * from claim;")
    except connector.Error as e :
        print("Exception" , e)
    return cur.fetchAll()

#customerlistclaim
def CustomerListClaim (customerId) :
    try:
        cur.execute(f"select * from claim where CustomerId={customerId};")
    except connector.Error as e :
        print("Exception" , e)
    return cur.fetchAll()


def planlist():
    try:
        cur.execute('select planid,type from plan;')
    except connector.Error as e:
        print("exception", e)
    return(cur.fetchall())
planlist()
def plandetails(id):
    try:
        cur.execute(f'select type,description,name,website,country,region,city,street, from plan,hospitalplan,hospital where plan.planid=hospitalplan.planid and hospitalid=hospitalplanid and plan.planid={id};')
    except connector.Error as e:
        print("exception", e)
    return cur.fetchall()
def ClaimDetail(id):
    try:
        cur.execute(f'select name,country,region,city,street,customerid,approved,submittingdate,expense,description,firstname,lastname from customer,claim,hospital where claimid= {id} and claim.customerid=customer.customerid and hospital.hospitalid=claim.hospitalid and claim.customerid=customer.customerid;')
    except connector.Error as e:
        print("exception", e)
    return cur.fetchall()
def getcontact(id):
    try:
        cur.execute(f'select holderid from customer where customer.customerid={id};')
    except connector.Error as e:
        print("exception", e)
    records = cur.fetchall()[0][1]
    try:
        cur.execute(f'select phone from customercontact where customer.customerid={records};')
    except connector.Error as e:
        print("exception", e)
    return cur.fetchall()