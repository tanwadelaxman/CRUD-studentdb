from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/Student_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
db = SQLAlchemy(app)
app.secret_key = "laxman"


class STUDENT(db.Model):
    STUDENT_NO = db.Column(db.Integer, primary_key=True)
    STUDENT_NAME = db.Column(db.TEXT,nullable = False)
    STUDENT_DOB = db.Column(db.DateTime(),default=datetime.now)
    STUDENT_DOJ = db.Column(db.DateTime(),default=datetime.now)


@app.route("/", methods=["GET", "POST"])
def student():
    if (request.method == "POST"):
        student_name = request.form.get("student_name")
        student_dob = request.form.get("student_dob")
        student_doj = request.form.get("student_doj")
        entry = STUDENT(STUDENT_NAME=student_name, STUDENT_DOB=student_dob, STUDENT_DOJ=student_doj)
        db.session.add(entry)
        db.session.commit()
    return render_template("index.html")

@app.route('/users', methods=['POST', 'GET'])
def view_users():
    entry = STUDENT.query.all()
    return render_template('users.html', entry=entry)


@app.route("/update/<STUDENT_NO>", methods=["GET"])
def edit(STUDENT_NO):
    entry = STUDENT.query.filter_by(STUDENT_NO =STUDENT_NO ).first()
    return render_template('update.html', entry = entry)


@app.route("/update", methods=["POST"])
def update():
    STUDENT_NO = request.form.get("student_no")
    STUDENT_NAME = request.form.get("student_name")
    STUDENT_DOB= request.form.get("student_dob")
    STUDENT_DOJ = request.form.get("student_doj")

    entry = STUDENT.query.filter_by(STUDENT_NO=STUDENT_NO).first()

    entry.STUDENT_NAME = STUDENT_NAME
    entry.STUDENT_DOB = STUDENT_DOB
    entry.STUDENT_DOJ = STUDENT_DOJ
    db.session.commit()
    return redirect('/users')


@app.route("/delete", methods=["POST"])
def delete():
    STUDENT_NO = request.form.get("STUDENT_NO")
    entry = STUDENT.query.filter_by(STUDENT_NO=STUDENT_NO).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)