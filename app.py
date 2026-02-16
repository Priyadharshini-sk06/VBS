from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key"  # required for session
# ======================
# BASIC PAGES
# ======================

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/choose/<mode>')
def choose_mode(mode):
    session['mode'] = mode   # store user choice
    return redirect(url_for('login'))

@app.route("/userguide")
def userguide():
    return render_template("userguide.html")

@app.route("/connectwithus", methods=["GET", "POST"])
def connectwithus():
    if request.method == "POST":
        # you can store data later
        return redirect(url_for("home"))
    return render_template("connectwithus.html")

# ======================
# AUTH
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # assume login success here

        mode = session.get("mode")

        if mode == "sign2speak":
            return redirect("/sign2speech")   # ✅ flipped
        elif mode == "speech2sign":
            return redirect("/speech2sign")   # ✅ flipped
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect(url_for("login"))
    return render_template("register.html")

# ======================
# FLOW PAGES
# ======================

@app.route("/sign2speech", methods=["GET", "POST"])
def sign2speech():
    if request.method == "POST":
        # later you can process form data here
        print("POST RECEIVED")
        return redirect(url_for("mode_select"))
    return render_template("sign2speech.html")

@app.route("/mode-select")
def mode_select():
    return render_template("mode-select.html")

@app.route("/practice")
def practice():
    return render_template("practice.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

@app.route("/meeting-setup")
def meeting_setup():
    return render_template("meeting-setup.html")

@app.route("/qa")
def qa():
    return render_template("qa.html")


@app.route("/speech2sign")
def speech2sign():
    return render_template("speech2sign.html")

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect,session
# from db import cursor,conn

# app = Flask(__name__)
# # requires to mantain session for individual user
# # app.secret_key = "stwos"

# # ----------------------home-----------------------------------------------------------------------------------------
# @app.route("/")
# @app.route("/home")
# def home():
  
#     return render_template("home.html")
# # --------------------userguide--------------------------------------------------------------------------------
# @app.route("/userguide")
# def userguide():
#     return render_template("userguide.html")
# # ---------------------------------------sign2speech-------------------------------------------------------------
# @app.route("/sign2speech")
# def sign2speech():
#     return render_template("sign2speech.html")
# # ---------------------------------------speech2sign-------------------------------------------------------------
# @app.route("/speech2sign")
# def speech2sign():
#     return render_template("speech2sign.html")



# # ------------------------login-----------------------------------------------------------------------------------


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         return render_template("login.html", message="")

#     uname = request.form["uname"]
#     pwd   = request.form["pwd"]

#     cursor.execute(
#         "SELECT password,user_Id FROM User_Details WHERE user_Name=%s",
#         (uname,)
#     )
#     res = cursor.fetchone()

#     if res and res["password"] == pwd:
#         # session["customer_id"] = res["user_Id"]
#         return redirect("/sign2speech")

#     return render_template("login.html", message="Invalid login")

# # -----------------------register---------------------------------------------------------------------------


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "GET":
#         return render_template("register.html", message="")

#     uname = request.form["uname"]
#     phone = request.form["phone"]
#     mail  = request.form["mail"]
#     pwd   = request.form["pwd"]
    
#     # print("REGISTER DATA:", uname, phone, mail, pwd)


#     cursor.execute(
#         "SELECT * FROM User_Details WHERE user_Name=%s",
#         (uname,)
#     )
#     if cursor.fetchone():
#         return render_template("register.html", message="Username already exists")

#     cursor.execute(
        
#         "INSERT INTO User_Details (user_Name, phoneNum, email, password) VALUES (%s,%s,%s,%s)",(uname, phone, mail, pwd)
#     )
#     conn.commit()
#     return redirect("/login")


# # ---------------connectwithus-----------------------

# # connectwithus page connection db
# @app.route("/connectwithus", methods=["GET", "POST"] )
# def connectwithus():
#     if request.method == "GET":
#         return render_template("connectwithus.html", )
   
#     con_name = request.form["con_name"]
#     con_no = request.form["con_no"]
#     con_email = request.form["con_email"]
#     con_query = request.form["con_query"]
#     con_feedback = request.form["con_feedback"]
#     cursor.execute(
#     "INSERT INTO contact_us (con_name,con_no ,con_email,con_query,con_feedback) VALUES (%s,%s,%s,%s,%s)",
#         (con_name,con_no , con_email, con_query, con_feedback)
#     )

#     conn.commit()

#     return render_template("connectwithus.html", message="Thank you for connecting with HerbalGlow .Your message means a lot to us. We'll get in touch very soon!")



# if __name__ == "__main__":
#     app.run(debug=True)
