from flask import Flask, request, render_template, redirect, url_for,session,flash
import mysql.connector
mydb= mysql.connector.connect(host='bp2l5vhn6siegz1ldmh2-mysql.services.clever-cloud.com',user='u7o4e3veisc7fz1i',passwd='aWxZSRii76R3d2yR6kIs', database='bp2l5vhn6siegz1ldmh2')
app = Flask(__name__)
app.secret_key = 'khaasservices'

@app.route('/')
def home():
    return render_template('index4.html')

@app.route('/customer-login', methods=['GET','POST'])
def customer_login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        cur=mydb.cursor()
        cur.execute("Select fullname,emailid,password,address,pincode from customerlogin where emailid = %s and password = %s " , (email,password))
        result=cur.fetchone()
        mydb.commit()
        cur.close()
        if result:
            session['user'] = { 'name' : result[0], 'email' : result[1], 'password' : result[2], 'address': result[3], 'pincode': result[4] }
            flash('Login successful!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('customer_login'))
    return render_template("customerlogin.html")



@app.route('/customer-register',methods=['POST'])
def customer_register():
    if request.method == 'POST':
        fullname = request.form['name']
        emailid = request.form['email']
        password = request.form['password']
        address = request.form['address']
        pincode= request.form['pincode']
        cur=mydb.cursor()
        cur.execute("INSERT INTO customerlogin (fullname, emailid, password, address, pincode) values (%s,%s,%s,%s,%s)",(fullname,emailid,password,address,pincode))
        mydb.commit()
        cur.close()
        return redirect ('/customer-login')
    return render_template('customerregister.html')

@app.route('/homepage')
def homepage():
    if 'user' in session:
        user= session['user']
        return render_template ('homepage.html' , user=user)
    else:
        return redirect(url_for('customer_login'))
    
@app.route('/proregister',methods=['GET','POST'])
def proregister():
    if request.method == 'POST':
        fullname = request.form['name']
        emailid = request.form['email']
        password = request.form['password']
        servicename= request.form['Servicename']
        experience= request.form['experience']
        address = request.form['address']
        pincode= request.form['pincode']
        cur=mydb.cursor()
        cur.execute("INSERT INTO prologin (fullname, emailid, password,servicename,experience, address, pincode) values (%s,%s,%s,%s,%s,%s,%s)",(fullname,emailid,password,servicename,experience,address,pincode))
        mydb.commit()
        cur.close()
        return redirect(url_for('pro_login'))
    return render_template('proregister.html')

@app.route('/pro-login', methods=['GET','POST'])
def pro_login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        cur=mydb.cursor()
        cur.execute("Select fullname,emailid,password,servicename,experience,address,pincode from prologin where emailid = %s and password = %s " , (email,password))
        result=cur.fetchone()
        mydb.commit()
        cur.close()
        if result:
            session['user'] = { 'name' : result[0], 'email' : result[1], 'password' : result[2],'servicename':result[3],'experience':result[4], 'address': result[5], 'pincode': result[6] }
            flash('Login successful!', 'success')
            return redirect(url_for('prohomepage'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('pro_login'))
    return render_template("prologin.html")

@app.route('/pro-homepage')
def prohomepage():
    if 'user' in session:
        user= session['user']
        return render_template ('prohomepage.html' , user=user)
    else:
        return redirect(url_for('/pro_login'))
@app.route('/profile', methods=['POST','GET'])
def profile():
    if 'user' in session:
        user= session['user']
        return render_template ('profile.html' , user=user)



if __name__ == '__main__':
    app.run(debug=True)