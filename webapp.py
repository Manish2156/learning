from flask import Flask ,render_template ,request , redirect , session , flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt



app = Flask(__name__)
app.secret_key="unkown"
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:123@localhost:5432/WEBSITE DATA"
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50) )
    password = db.Column(db.String(255))
    number = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
@app.route("/")
def root():
    return redirect("/base")
@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/base/register")
def register():
    return render_template("register.html")

@app.route("/base/register-user"  , methods=["POST"])
def reguser():
    
    name = request.form["name"]
    phn = int(request.form["phone_no"])
    email = request.form["email"]
    user = User.query.filter_by(email=email).first()
    if user is None : 
        password = request.form["password"]
        cf_password = request.form["confirm_password"]
        if password == cf_password :
            hpass = bcrypt.hashpw(password.encode("utf-8") , bcrypt.gensalt()).decode("utf-8")
            user = User(
                name = name ,
                email = email,
                password = hpass,
                number = phn
            )
            db.session.add(user)
            db.session.commit()
            flash("Registered Successfully")
        else :
            flash("Password did not match")
            return redirect("/base/register")
    else :
        flash("Email already registered")
        return redirect("/base/register")
        

@app.route("/base/login")
def login():
    return render_template("login.html")

@app.route("/base/login-user" , methods=["POST"])
def loguser():
    email= request.form["email"]
    pas = request.form["password"]
    user = User.query.filter_by(email=email).first()
    if user is None :
        flash("Email is not Registered")
        return redirect("/base/login")
    else :
        if bcrypt.checkpw(pas.encode("utf-8") , user.password.encode("utf-8")):
            session["ss_id"] = user.id
            flash("Logged In")
            return redirect("/base/home")
        else :
            flash("Wrong Password")
            return redirect("/base/login")

@app.route("/base/home" , methods =["GET"])
def home():
    user = User.query.get(session["ss_id"])

    return render_template("home.html" , user=user)

if __name__ == "__main__":
    app.run(debug=True)
