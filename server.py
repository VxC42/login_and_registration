from flask import Flask, request, redirect, render_template, session, flash
from validations import formIsValid
from mysqlconnection import MySQLConnector
import md5
app = Flask(__name__)
app.secret_key="secretsrunsdeep"

mysql = MySQLConnector(app, 'registration')


@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/register', methods=['POST'])
def register():
    state = formIsValid(request.form)
    if (state['isValid']):
        password = encrypted_password = md5.new(request.form['pw']).hexdigest();
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email': request.form['email'],
            'password': password
            }
        result=mysql.query_db(query, data)

        query2 = "SELECT * FROM users WHERE id = :id"
        data2={'id' : result}
        user = mysql.query_db(query2, data2)

        return render_template('/profile.html', user=user[0])
    else:
        for error in state['errors']:
            flash(error)
            print error
            return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    password = encrypted_password = md5.new(request.form['pw']).hexdigest();
    query = "SELECT * FROM users WHERE email = :email AND password = :password"
    data = {
        'email': request.form['email'],
        'password':password
    }
    result= mysql.query_db(query, data)
    if len(result) >0:
        return render_template('/profile.html', user=result[0])
    else:
        flash("Couldn't find you.")
        return redirect('/')

@app.route('/logout/<id>', methods=['POST'])
def logout(id):
    session['first_name']=''
    session['last_name']=''
    session['email']=''
    session['password']=''
    session['created_at']=''
    session['updated_at']=''
    session['id']=''
    return redirect('/')





app.run(debug=True)
