#importing the needed packages
from flask import Flask, request, session, redirect, render_template
from pymongo import MongoClient
from werkzeug.security import check_password_hash , generate_password_hash
from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from bson import ObjectId
import os , random , smtplib

now = datetime.now()
app = Flask(__name__)
load_dotenv()
#for hiding secert details from public
app.secret_key = os.getenv("key")
MONGO_URL = os.getenv("MONGO_URL")
adminuser = os.getenv("ADMIN_USER")
adminpass = os.getenv("ADMIN_PASS")
apppass = os.getenv("APP_PASS")
# defining variable's for user interaction 
flag = False
boo = 0
notboo = 0
loginerror=0
global adminbool
#connecting app to Mongodb Atlas
client = MongoClient(MONGO_URL)
db = client["gadnexus"]
users = db["users"]
posts= db["posts"]



#defining the needed route's
@app.route("/")
@app.route("/index")
def index():
    data = list(posts.find().sort("created_at",-1)) #to sort the posts in Antichronological order
    if("username" in session):
        boo =1
        notboo = 0
    else:    
        boo=0
        notboo = 1
    return render_template("index.html",data=data,boo=boo,notboo=notboo)

@app.route("/login",methods=["POST","GET"])
def login():
    if(request.method=="POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.find_one({"username" : username})
        if(user and check_password_hash(user["password"],password)):
            session["username"]=username
            return redirect("/dashboard")
        else:
            return render_template("error.html",error = "Username or Password is Incorrect !",loginerror=1)
    return render_template("login.html", flag = False)

@app.route("/register",methods=["POST","GET"])
def reg():
        if(request.method=="POST"):
            username = request.form.get("username")
            password = request.form.get("password")
            email = request.form.get("email")
            fname = request.form.get("fname")
            if(users.find_one({"username":username})):
                return render_template("error.html",error="The user already Exits ! Please Log In")
            hashpassword = generate_password_hash(password)
            user = {"username":username , "password":hashpassword , "email":email,"fname":fname}
            users.insert_one(user)
            return render_template("login.html",flag=True,message="Account Created , Please Login !")
        else:
            return render_template("register.html") 
    
@app.route("/dashboard")
def dash():
    
    if("username" in session):
        data = list(posts.find({"username":session["username"]}))
        return render_template("dashboard.html",user=session["username"],data=data)
    else:
            return render_template("error.html",error="Please Log In !")

@app.route("/dashboard/delete",methods=["POST"])
def delete():
    id = request.form.get("id")
    document = posts.find_one({"_id":ObjectId(id)})
    posts.delete_one(document)
    return redirect("/dashboard")

@app.route("/dashboard/edit/",methods=["POST","GET"])
def edit():
    
    if(request.method=="GET"):
        id = request.args.get("id")
        document = posts.find_one({"_id":ObjectId(id)})
        return render_template("edit.html",post=document)
    else:   
        id = request.form.get("id")    
        document = posts.find_one({"_id":ObjectId(id)})
        title = request.form.get("title")
        description = request.form.get("description")
        image_url = request.form.get("image_url")
        date = now.strftime("%B %Y")
        dbuser = users.find_one({"username":session["username"]})
        user = dbuser["fname"]
        post = {"title":title , "description":description , "date":date ,"fname":user,"username":session['username'], "created_at": datetime.utcnow()}   
        posts.update_one(
            { '_id': ObjectId(id)},
            { '$set' :post}
        ) 
        return redirect('/dashboard')

@app.route("/logout",methods=["POST","GET"])
def logout():
    if ("username" in session):
        session.pop("username", None)
        return redirect("/")
    else:
        return render_template("error.html",error="Please Log In First !")

@app.route("/reset", methods=["POST","GET"])
def reset():
     if(request.method=="POST"):
        username = request.form.get("username")
        newpassword = request.form.get("newpassword")
        newhash_password = generate_password_hash(newpassword)
        email  = request.form.get("email")
        user = users.find_one({"username":username , "email":email})
        if(user):
            users.update_one(
                {"username": username},
                {"$set": {"password": newhash_password}})
            return render_template("login.html",flag=True,message="Account Reset Succesfull !")
        else:
            return render_template("error.html",error="Email or Username Not Found !")  
     else:     
        return render_template("reset.html")

@app.route("/dashboard/upload",methods=["POST","GET"])
def post_upload():
    if("username" in session):
        if(request.method=="POST"):
            title = request.form.get("title")
            description = request.form.get("description")
            image_url = request.form.get("image_url")
            date = now.strftime("%B %Y")
            dbuser = users.find_one({"username":session["username"]})
            user = dbuser["fname"]
            post = {"title":title , "description":description , "date":date ,"fname":user,"username":session['username'], "created_at": datetime.utcnow()}
            posts.insert_one(post)
            return redirect("/dashboard")
        else:
            return render_template("postupload.html")   
    else:
            return render_template("error.html",error="Please Log In !")

@app.route("/admin",methods=["POST","GET"])
def admin():
    if(request.method=="POST"):    
        email = request.form.get("email")
        password = request.form.get("password")
        if (email==adminuser and password==adminpass):
            otp = random.randint(100000,999999)
            session["otp"]=str(otp)
            send_otp(email,otp)
            return render_template("verify-otp.html")
        else:
            return render_template("error.html",error="You Are Not An Admin !") 
    else:       
        return render_template("admin.html")
    
@app.route("/verify-otp",methods=["POST","GET"])
def otp():
    if(request.method=="POST"):
        otp = request.form.get('otp')
        if(otp==session["otp"]):
            global adminbool
            adminbool = 1
            return redirect("/admin-page")
        else:
            return render_template("verify-otp.html", flag=True,message="Incorrect OTP , Please try Again !")
    else:
        return render_template("verify-otp.html")    

@app.route("/admin-page")
def adpag():
    if(adminbool):
        data = list(posts.find())
        return render_template("admin-page.html",data=data)
    else:
        return render_template("error.html",error="Please Sign In as an Admin !")

@app.route("/adminlogout",methods=["POST"])
def adminlogout():
    global adminbool
    adminbool = 0
    return redirect('/')

def send_otp(receiver_email,otp):
    sender = adminuser
    app_pass = apppass
    message = MIMEText(f"Your ADMIN OTP Code For GadNEXUS Is: {otp} , Please Dont Reply To This Message .")
    message['Subject'] = "Your Admin OTP Code"
    message['From'] = sender
    message['To'] = receiver_email

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  
        server.starttls()  # Enable TLS encryption
        server.login(sender, app_pass)
        server.sendmail(sender, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False


#for debugging
if(__name__=="__main__"):
    app.run(debug=True)