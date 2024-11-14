from flask import Flask, request, render_template, redirect, url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
from models import db, User, Service, ServiceRequest
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize the database
with app.app_context():
    db.create_all()


# import mysql.connector
# mydb= mysql.connector.connect(host='bp2l5vhn6siegz1ldmh2-mysql.services.clever-cloud.com',user='u7o4e3veisc7fz1i',passwd='aWxZSRii76R3d2yR6kIs', database='bp2l5vhn6siegz1ldmh2')
# app = Flask(__name__)
# app.secret_key = 'khaasservices'

@app.route('/')
def home():
    return render_template('index4.html')

@app.route('/customer-login', methods=['GET','POST'])
def customer_login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user = User.query.filter_by(username=email).first()
        if user and user.password == password:
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user.role == "professional":
                return redirect(url_for("professional_dashboard"))
            elif user.role == "customer":
                return redirect(url_for("customer_dashboard"))
        else:
            return "Invalid credentials"        
        # cur=mydb.cursor()
        # cur.execute("Select fullname,emailid,password,address,pincode from customerlogin where emailid = %s and password = %s " , (email,password))
        # result=cur.fetchone()
        # mydb.commit()
        # cur.close()
        # if result:
        #     session['user'] = { 'name' : result[0], 'email' : result[1], 'password' : result[2], 'address': result[3], 'pincode': result[4] }
        #     flash('Login successful!', 'success')
        #     return redirect(url_for('homepage'))
        # else:
        #     flash('Invalid credentials. Please try again.', 'error')
        #     return redirect(url_for('customer_login'))
    return render_template("customerlogin.html")



@app.route('/customer-register',methods=['GET','POST'])
def customer_register():
    if request.method == 'POST':
        fullname = request.form['name']
        emailid = request.form['email']
        password = request.form['password']
        address = request.form['address']
        pincode= request.form['pincode']
        # cur=mydb.cursor()
        # cur.execute("INSERT INTO customerlogin (fullname, emailid, password, address, pincode) values (%s,%s,%s,%s,%s)",(fullname,emailid,password,address,pincode))
        # mydb.commit()
        # cur.close()
        new_user = User(username=emailid, password=password, role='customer')
        db.session.add(new_user)
        db.session.commit()
        return redirect ('/customer-login')
    return render_template('customerregister.html')


@app.route('/proregister',methods=['GET','POST'])
def proregister():
    if request.method == 'POST':
        fullname = request.form['name']
        emailid = request.form['email']
        password = request.form['password']
        servicename= request.form['Servicename']
        price=request.form['price']
        time=request.form['time']
        description=request.form['description']
        experience= request.form['experience']
        address = request.form['address']
        pincode= request.form['pincode']
        # cur=mydb.cursor()
        # cur.execute("INSERT INTO prologin (fullname, emailid, password,servicename,experience, address, pincode) values (%s,%s,%s,%s,%s,%s,%s)",(fullname,emailid,password,servicename,experience,address,pincode))
        # mydb.commit()
        # cur.close()
        new_user = User(username=emailid, password=password, role='professional')
        new_service=Service(name=servicename,price=price,time_required=time,description=description)
        db.session.add(new_user)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('customer_login'))
    return render_template('proregister.html')

# @app.route('/pro-login', methods=['GET','POST'])
# def pro_login():
#     if request.method == 'POST':
#         email=request.form['email']
#         password=request.form['password']
#         cur=mydb.cursor()
#         cur.execute("Select fullname,emailid,password,servicename,experience,address,pincode from prologin where emailid = %s and password = %s " , (email,password))
#         result=cur.fetchone()
#         mydb.commit()
#         cur.close()
#         if result:
#             session['user'] = { 'name' : result[0], 'email' : result[1], 'password' : result[2],'servicename':result[3],'experience':result[4], 'address': result[5], 'pincode': result[6] }
#             flash('Login successful!', 'success')
#             return redirect(url_for('professional_dashboard'))
#         else:
#             flash('Invalid credentials. Please try again.', 'error')
#             return redirect(url_for('pro_login'))
#     return render_template("prologin.html")


#DASHBOARDS#

@app.route('/customer/dashboard')
@login_required
def customer_dashboard():
    # if 'user' in session:
    #     user= session['user']
    #     return render_template ('customer_dashboard.html' , user=user)
    if current_user.role != "customer":
        return redirect(url_for("customer_login"))
    # else:
    #     return redirect(url_for('customer_login'))

    services = Service.query.all()
    service_requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    return render_template("customer_dashboard.html", services=services, service_requests=service_requests, user=current_user)

@app.route("/customer/request_service", methods=["GET", "POST"])
@login_required
def request_service():
    if current_user.role != "customer":
        return redirect(url_for("customer_login"))
    services = Service.query.all()
    if request.method == "POST":
        service_id = request.form["service_id"]
        new_request = ServiceRequest(
            service_id=service_id,
            customer_id=current_user.id,
            service_status="requested"
        )
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for("customer_dashboard"))
    return render_template("request_service.html", services=services)

@app.route("/customer/cancel_service_request/<int:request_id>", methods=["POST"])
@login_required
def cancel_service_request(request_id):
    # Ensure that only the customer who created the request can cancel it
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.customer_id != current_user.id:
        flash("You are not authorized to cancel this service request.", "error")
        return redirect(url_for("customer_dashboard"))
    
    # Update the status to "canceled" (or delete if required)
    service_request.service_status = "canceled"
    db.session.commit()
    flash("Service request canceled successfully.", "success")
    return redirect(url_for("customer_dashboard"))


@app.route('/professional/dashboard')
@login_required
def professional_dashboard():
    if current_user.role != "professional":
        return redirect(url_for("customer_login"))
    
    # View only requests assigned to this professional
    service_requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
    return render_template("professional_dashboard.html", service_requests=service_requests)

    # if 'user' in session:
    #     user= session['user']
    #     return render_template ('professional_dashboard.html' , user=user)
    # else:
    #     return redirect(url_for('/pro_login'))


@app.route("/professional/accept_request/<int:request_id>", methods=["POST"])
@login_required
def accept_request(request_id):
    if current_user.role != "professional":
        return redirect(url_for("customer_login"))
    
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.service_status == "requested":
        service_request.professional_id = current_user.id
        service_request.service_status = "assigned"
        db.session.commit()
    return redirect(url_for("professional_dashboard"))

@app.route("/professional/reject_request/<int:request_id>", methods=["POST"])
@login_required
def reject_request(request_id):
    if current_user.role != "professional":
        return redirect(url_for("sutomer_login"))
    
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.service_status == "requested":
        service_request.service_status = "rejected"
        db.session.commit()
    return redirect(url_for("professional_dashboard"))

    
@app.route("/professional/complete_request/<int:request_id>", methods=["POST"])
@login_required
def complete_request(request_id):
    if current_user.role != "professional":
        return redirect(url_for("customer_login"))
    
    service_request = ServiceRequest.query.get(request_id)
    if service_request and service_request.service_status == "assigned" and service_request.professional_id == current_user.id:
        service_request.service_status = "completed"
        db.session.commit()
    return redirect(url_for("professional_dashboard"))

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return redirect(url_for("customer_login"))
    users = User.query.all()
    services = Service.query.all()
    return render_template("admin_dashboard.html", users=users, services=services)

@app.route("/admin/service/new", methods=["GET", "POST"])
@login_required
def new_service():
    if current_user.role != "admin":
        return redirect(url_for("customer_login"))
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        time_required = request.form["time_required"]
        description = request.form["description"]
        new_service = Service(name=name, price=price, time_required=time_required, description=description)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("new_service.html")



@app.route('/profile', methods=['POST','GET'])
def profile():
    if 'user' in session:
        user= session['user']
        return render_template ('profile.html' , user=user)



if __name__ == '__main__':
    app.run(debug=True)