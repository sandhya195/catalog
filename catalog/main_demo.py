from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iiit.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

app=Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='sandhyakolakaluri@gmail.com'
app.config['MAIL_PASSWORD']='s@ndhy@1249'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key='=abc'

mail=Mail(app)
otp=randint(000000,999999)



def demo():
	return "Hello World welcome to my world"


@app.route("/demo_msg")
def d():
	return "<h1>Hello Demo Page</h1>"


@app.route("/info/details")
def i():
	return "<h2>Hello Details</h2>"

@app.route("/details/<name>/<int:age>/<float:salary>")
def info(name,age,salary):
	return "Hello {} age {} and salary {}".format(name,age,salary)

@app.route("/admin")
def a():
	return "Hello Admin"

@app.route("/student")
def student():
	return "Hello student"

@app.route("/staff")
def staff():
	return "Hello staff"


@app.route("/info/<name>")
def admin_info(name):
	if name=='admin':
		return redirect(url_for('admin'))

	elif name=='student':
		return redirect(url_for('student'))
	elif name=='staff':
		return redirect(url_for('staff'))
	else:
		return "<h2 style='color:red'>Not a valid URL..!</br>Check it...!!</h2>"

@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_html1(name,age,salary):
	return render_template('sampletable.html',n=name,a=age,s=salary)

@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_html(name,age,salary):

	return render_template('sampletable.html',n=name,a=age,s=salary)

@app.route("/info-data")
def info_data():
	sno=28
	name='Sandhya'
	Branch='CSE'
	return render_template('sampletable.html',s_no=sno,n=name,b=branch,d=dept)

data=[{'sno':123,'name':'Sandhya','branch':'CSE','dept':'engg-3'},
{'sno':124,'name':'Rani','branch':'CSE','dept':'engg-3'}]

@app.route("/dummy_data")
def dummy():
	return render_template('sampletable.html',dummy_data=data)

@app.route("/table/<int:number>")
def table(number):
	return render_template("table.html",n=number)

@app.route("/file_upload", methods=['GET','POST'])
def file_upload():
	return render_template("file_upload.html")

@app.route("/success", methods=['GET','POST'])
def success():
	if request.method=='POST':
	   f=request.files['file']
	   f.save(f.filename)
	return render_template("success.html",f_name=f.filename)

@app.route("/email", methods=['POST','GET'])
def email_send():
	return render_template("email.html")

@app.route("/email_verify", methods=['POST','GET'])
def verify_email():
	email=request.form['email']
	msg=Message('One Time Password', sender='sandhyakolakaluri@gmail.com', recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template("v_email.html")

@app.route("/email_success",methods=['POST','GET'])
def success_email():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		return render_template("email_success.html")
	return "Invalid otp"

@app.route("/show")
def showData():
	register=session.query(Register).all()

	return render_template('show.html',reg=register)
@app.route("/reg_page")
def regData():
	return render_template('reg_page.html')


@app.route("/new",methods=['POST','GET'])
def insertData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			surname=request.form['surname'],
			mobile=request.form['mobile'],
			email=request.form['email'],
			branch=request.form['branch'],
			role=request.form['role'])
		session.add(newData)
		session.commit()
		flash("New Data added....")
		return redirect(url_for('showData'))
	else:
		return render_template("new.html")

@app.route("/")
def navigation():
	return render_template("navbar.html")

@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editedData.name=request.form['name']
		editedData.surname=request.form['surname']
		editedData.mobile=request.form['mobile']
		editedData.email=request.form['email']
		editedData.branch=request.form['branch']
		editedData.role=request.form['role']

		session.add(editedData)
		session.commit()
		flash("edited Data of {}".format(editedData.name))

		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editedData)

@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
	deleteData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		session.delete(deleteData)
		session.commit()
		flash("Deleted data of{}".format(deleteData.name))

		return redirect(url_for('showData'))
	else:
		return render_template('delete.html',register=deleteData)








if __name__ == '__main__':
	app.run(debug=True)