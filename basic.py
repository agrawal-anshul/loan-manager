from flask import Flask,render_template,request,redirect, url_for, session
from flaskext.mysql import MySQL
from flask_login import login_required
from pymysql.cursors import DictCursor


import re
app=Flask(__name__)

#Connection to mysql
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345'
app.config['MYSQL_DATABASE_DB'] = 'loandb'
app.secret_key = 'mysecretkey'

mysql = MySQL(cursorclass=DictCursor)

mysql.init_app(app)

@app.route("/")
def index():
    '''conn = mysql.connect()
    cursor =conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS Athlete( Athlete_ID int(11) NOT NULL,Athlete_FirstName varchar(45) NOT NULL,Athlete_LastName varchar(45) NOT NULL,Athlete_DOB date NOT NULL,Athlete_Gender varchar(10) NOT NULL,Country_Code int(11) NOT NULL ,PRIMARY KEY (Athlete_ID))"
    query1= "CREATE TABLE IF NOT EXISTS Result( Athlete_ID int(11) NOT NULL,Medal_Type varchar(30) not null ,Sports_Name varchar(100) not null,PRIMARY KEY(Athlete_ID))"
    query2= "CREATE TABLE IF NOT EXISTS Country( Country_Code int(11) NOT NULL,Country_Name varchar(50) NOT NULL,Primary key(Country_Code))"
    query3= "CREATE TABLE IF NOT EXISTS Schedule(  Athlete_ID int(11) NOT NULL,Date date NOT NULL,Time time NOT NULL,Venue varchar(20) not null,Sports_Name varchar(100) not null,Primary key(Athlete_ID))"
    query5= "CREATE TABLE IF NOT EXISTS Site(Country_Code int(11) NOT NULL,Year int(5) not null,City varchar(20) not null,Season varchar(20) not null)"
    #query6= "alter table Athlete add foreign key(Country_Code) references Country(Country_Code) on update cascade on delete cascade"
    #query7= "alter table Result add foreign key(Athlete_ID) references Athlete(Athlete_ID) on update cascade on delete cascade"
    #query8= "alter table Result  add foreign key(Athlete_ID) references Schedule(Athlete_ID)"
    #query9= "alter table Site add foreign key(Country_Code) references Country(Country_Code) on update cascade on delete cascade"
    cursor.execute(query)
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
   
    cursor.execute(query5)
    #cursor.execute(query6)
    #cursor.execute(query7)
    #cursor.execute(query8)
    #cursor.execute(query9)
    cursor.close()'''
    
    
    return render_template('index.html')
@app.route("/admin",methods=['GET', 'POST'])
def admin():
    conn = mysql.connect()
    cursor =conn.cursor()
    
    query="CREATE TABLE IF NOT EXISTS accounts (id int(11) NOT NULL AUTO_INCREMENT,username varchar(50) NOT NULL,password varchar(255) NOT NULL,email varchar(100) NOT NULL,PRIMARY KEY (id))"
    cursor.execute(query)
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
      
        email = request.form['email']
        password = request.form['password']
    
        admin="admin"

        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s and cname= %s and role= %s', (email,password,admin,admin))
       
        account = cursor.fetchone() 
        
       
        if account:
            session['loggedin'] = True
            session['id'] = account['email']
            session['username'] = account['password']
            return render_template("login.html")
        else:

            msg = 'Incorrect username/password!'
    
    return render_template("admin.html",msg=msg)
@app.route("/customer",methods=['GET', 'POST'])
def customer():
    conn = mysql.connect()
    cursor =conn.cursor()
    query="CREATE TABLE IF NOT EXISTS accounts (id int(11) NOT NULL AUTO_INCREMENT,cname varchar(50) NOT NULL,password varchar(255) NOT NULL,email varchar(100) NOT NULL,PRIMARY KEY (id))"
    cursor.execute(query)
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
      
        email = request.form['email']
        password = request.form['password']
        ct="customer"

        
        
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s and role= %s', (email,password,ct))
       
        account = cursor.fetchone() 
        
        
       
        if account:
            session['loggedin'] = True
            # session['id'] = account['email']
            # session['username'] = account['password']
            session['profile_email']=account['email']
            session['profile_username']=account['cname']
            
            return render_template("login2.html",account=account)
        else:

            msg = 'Incorrect username/password!'
    
    return render_template("customer.html",msg=msg)
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('email', None)
   session.clear()
   # Redirect to login page
   return render_template("index.html")
@app.route('/login1')
def login1():
    return render_template("login.html")
@app.route('/login2')
def login2():
    return render_template("login2.html")

@app.route('/viewcustomer')
def viewcustomer():
    conn = mysql.connect()
    cursor =conn.cursor()
    query="Select * from Customer"
    cursor.execute(query)
    cus=cursor.fetchall()
    
    return render_template("viewcustomer.html",cus=cus)

@app.route('/newcustomer')
def newcustomer():
    
    return render_template('newcustomerform.html')

@app.route('/newcustomer/post',methods=['GET', 'POST'])
def newcustomerpost():
    conn = mysql.connect()
    cursor=conn.cursor()
    print(request.form)
    account_no=request.form['accountNo']
    name=request.form['name']
    balance=request.form['balance']
    accounttype=request.form['accounttype']
    bno=request.form['bno']
    #email=request.form['email']
    phone=request.form['phoneNumber']
    address=request.form['address']
    print(account_no,name,balance,accounttype,bno)
    cursor.execute('INSERT INTO account (account_no,account_type,balance,bno) VALUES (%s,%s,%s,%s)',(account_no,accounttype,balance,bno,))
   
    conn.commit()

    sql="INSERT INTO customer (cname,address,phone,account_no) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql,(name,address,phone,account_no,))
    conn.commit()
    return redirect('viewcustomer')
@app.route('/newregister',methods=['GET', 'POST'])
def newregistercus():
    
    return render_template('newregistercus.html')

@app.route('/newregister/post',methods=['GET', 'POST'])
def newregistercuspost():
    conn = mysql.connect()
    cursor=conn.cursor()
    # print(request.form)
    username=request.form['username']

    email=request.form['email']
    password=request.form['password']
    role="customer"
   

    sql="INSERT INTO accounts (cname,password,email,role) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql,(username,password,email,role,))
    conn.commit()
    return redirect('login2')

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    conn = mysql.connect()
    cursor=conn.cursor()
    name=session['profile_username']
    cursor.execute('SELECT account_no FROM customer WHERE cname = %s', (name))
    account_no=cursor.fetchone()
    account_no=account_no['account_no']
  
    cursor.execute('SELECT balance FROM account WHERE account_no = %s', (account_no))
    balance=cursor.fetchone()
    balance=balance['balance']
    query="Select * from profile_data"
    cursor.execute(query)
    profile_data=cursor.fetchall()
    print(profile_data)
    for i in profile_data:
        name1=i['cname']
        print("S",name)
        print(name1)
        if(name==name1.lower()):
            new_data=i
            print(new_data)


   
    return render_template('profile.html',new_data=new_data,balance=balance)

@app.route('/applyloans',methods=['GET', 'POST'])
def applyloans():


    return render_template('applyloans.html')


@app.route('/applyloans/post',methods=['GET', 'POST'])
def applyloanspost():
    conn = mysql.connect()
    cursor=conn.cursor()
    
    loan_val=request.form['loan']
    map={"Home":2,"Car":1,"Bike":1,"Education":2}
    value=map[loan_val]
    print(value)
    amount=request.form['amount']
    doi=request.form['doi']
    timeperiod=request.form['timeperiod']
    banknumber=request.form['banknumber']
    name=session['profile_username']
    cursor.execute('SELECT account_no FROM customer WHERE cname = %s', (name))
    account_no=cursor.fetchone()
    account_no=account_no['account_no']
  

    sql="INSERT INTO loan (loan_type,amt,roi,doi,time_period,bno,account_no) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,(loan_val,amount,value,doi,timeperiod,banknumber,account_no,))
    conn.commit()
    return render_template('login2.html')


@app.route('/viewadminloans',methods=['GET', 'POST'])
def viewadminloans():
    conn = mysql.connect()
    cursor =conn.cursor()
    query="Select * from loan"
    cursor.execute(query)
    loan=cursor.fetchall()
    print(loan)
    
    return render_template("viewadminloans.html",loan=loan)


@app.route('/viewcustomerloans',methods=['GET', 'POST'])
def viewcustomerloans():
    conn = mysql.connect()
    cursor =conn.cursor()
    name=session['profile_username']
    cursor.execute('SELECT account_no FROM customer WHERE cname = %s', (name))
    account_no=cursor.fetchone()
    account_no=account_no['account_no'] 

    cursor.execute('SELECT * FROM loan WHERE account_no = %s', (account_no))
    loan=cursor.fetchall()
    # print(loan)     

    return render_template('viewcustomerloans.html',loan=loan)


@app.route('/loanpayment',methods=['GET', 'POST'])
def loanpayment():
    conn = mysql.connect()
    cursor =conn.cursor()
    name=session['profile_username']
    cursor.execute('SELECT account_no FROM customer WHERE cname = %s', (name))
    account_no=cursor.fetchone()
    account_no=account_no['account_no'] 
    loan_no=request.form['loan_no']
    cursor.execute("SELECT balance,amt,roi,time_period  FROM new where account_no=%s",(account_no))
    m=cursor.fetchone()
    balance=m['balance']
    amt=m['amt']
    roi=m['roi']
    time_period=m['time_period']
    balance=balance-(amt*((1+roi/100)**time_period))
    cursor.execute("UPDATE account, loan set account.balance =%s where loan.loan_no=%s and status = 'approved' and payment_status = 'unpaid'", (balance,loan_no))
    conn.commit()
    cursor.execute("UPDATE loan set  payment_status = 'paid' where loan.loan_no = %s and status = 'approved' and payment_status = 'unpaid'", (loan_no))
    conn.commit()
  

    return redirect('viewcustomerloans')




@app.route('/approveadminloans',methods=['GET', 'POST'])
def approveadminloans():
    conn = mysql.connect()
    cursor =conn.cursor()
    loan_no=request.form['loan_no']
    

    cursor.execute('UPDATE loan SET status ="approved" WHERE loan_no=%s;', (loan_no))
    conn.commit()
   
    return redirect('viewadminloans')



@app.route('/viewsuperloans',methods=['GET', 'POST'])
def viewsuperloans():
    conn = mysql.connect()
    cursor =conn.cursor()

    query="Select * from super_loans"
    cursor.execute(query)
    super_loan=cursor.fetchall()
    
    


    return render_template('viewsuperloans.html',super_loan=super_loan)

@app.route('/approvesuperloans',methods=['GET', 'POST'])
def approvesuperloans():
    conn = mysql.connect()
    cursor =conn.cursor()
    loan_no=request.form['loan_no']
    print(loan_no)

    cursor.execute('UPDATE super_loans SET status="approved" WHERE loan_no=%s;', (loan_no))
    cursor.execute('UPDATE loan SET status="approved" WHERE loan_no=%s;', (loan_no))
    conn.commit()
   
    return redirect('viewsuperloans')




if __name__ == "__main__":
    app.run(debug=True)