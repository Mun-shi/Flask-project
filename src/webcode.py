from flask import *
from src.dbconnect import *
from werkzeug.utils import secure_filename
import os
app=Flask(__name__)

app.secret_key="123"
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/')
def login():
    return render_template("login2.html")

@app.route('/registration')
def reg():

    return render_template("registration.html")

@app.route('/table')
def view():
    qry="SELECT * FROM registration"
    s=select(qry)
    return render_template("table.html",val=s)

@app.route('/update')
def update():
    id=session['lid']
    qry="select* from registration where lid=%s"
    val=(str(id))
    s=selectonecond(qry,val)
    print(s)

    return render_template("update.html",val=s)

@app.route('/userhome')
def user():
    return render_template("userhome.html")



@app.route('/register',methods=['post','get'])
def register():
        print (request.form)
        fname=request.form['firstname']
        lname = request.form['lastname']
        gender = request.form['gender']
        date = request.form['dob']
        address = request.form['address']
        quali = request.form.getlist('qualification' )
        qualification=(','.join(quali))
        state = request.form['state']
        image = request.files['file']
        file=secure_filename(image.filename)
        image.save(os.path.join(r'C:\Users\Hp\Desktop\vaccin\src\static/uplod',file))
        uname = request.form['username']
        password = request.form['password']
        qry="insert into login values(null,%s,%s,'user')"
        val=(uname,password)
        id=iud(qry,val)
        qry2="insert into registration values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values= (fname, lname, gender, date,address, qualification,state,file,id)
        iud(qry2,values)
        return '''<script>alert('registered');window.location='/'</script>'''


@app.route('/login2',methods=['post'])
def login2():
    uname=request.form['email']
    password=request.form['password']
    q="select*from login where uname=%s and password=%s"
    val=(uname,password)
    s=selectonecond(q,val)
    if s  is None:
        return '''<script>alert('Invalid user name or password');window.location='/'</script>'''
    elif s[3]=='admin':
        session['lid']=s[0]
        return '''<script>alert('login successfully');window.location='/home'</script>'''
    elif s[3] == 'user':
        session['lid'] = s[0]
        return '''<script>alert('login successfully');window.location='/userhome'</script>'''
    else:
        return '''<script>alert('invalid username or password');window.location='/'</script>'''

@app.route('/updatedata',methods=['post','get'])
def update1():
    try:
        id=session['lid']
        fname=request.form['firstname']
        lname =request.form['lastname']
        gender =request.form['gender']
        date=request.form['dob']
        address=request.form['address']
        quali=request.form.getlist('qualification')
        qualification=(','.join(quali))
        state=request.form['state']
        image = request.files['file']
        file = secure_filename(image.filename)
        image.save(os.path.join('./static/uplod', file))
        qry = "update registration set firstName=%s,lastName=%s,gender=%s,date=%s,address=%s,qualification=%s,state=%s,filename=%s where lid=%s"
        values = (fname, lname, gender, date,address, qualification,state,image,id)
        iud(qry, values)
        return '''<script>alert('Profile updated');window.location='/userhome'</script>'''
    except Exception as e:
        id=session['lid']
        fname=request.form['firstname']
        lname =request.form['lastname']
        gender =request.form['gender']
        date=request.form['dob']
        address=request.form['address']
        quali=request.form.getlist('qualification')
        qualification=(','.join(quali))
        state=request.form['state']

        qry = "update registration set firstName=%s,lastName=%s,gender=%s,date=%s,address=%s,qualification=%s,state=%s where lid=%s"
        values = (fname, lname, gender, date,address, qualification,state,id)
        iud(qry,values)
        return '''<script>alert('Profile updated');window.location='/userhome'</script>'''



@app.route('/delete')
def delete():
    id=request.args.get('id')
    print(id)
    q="delete from registration where id=%s"
    val=(id)
    iud(q,val)
    return '''<script>alert('deleted');window.location='/table'</script>'''









app.run(debug=True)




