from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/")
def index():
    return(render_template('index.html'))

@app.route("/users")
def users():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    return(render_template('users.html', users=users))    

@app.route("/users/new")
def make():
    return(render_template('new_users.html'))

@app.route("/users/add", methods=['POST'])
def add():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(FN)s, %(LN)s, %(EM)s, NOW(), NOW());"
    data = {
        'FN' : request.form['FN'],
        'LN' : request.form['LN'],
        'EM' : request.form['EM'],
    }
    test = connectToMySQL('users')
    test.query_db(query, data)
    return redirect("/users")

@app.route('/users/delete/<num>')
def remove(num):
    query = "DELETE FROM users WHERE id= %(id)s"
    data = {
        'id': num
    }
    test = connectToMySQL('users')
    test.query_db(query, data)
    return redirect("/users")

@app.route('/users/show/<user_id>')
def show(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s"
    data = {
        'id': user_id
    }
    mysql = connectToMySQL('users')
    user = mysql.query_db(query, data)
    return(render_template('show.html', user_id = user_id, user=user[0]))

@app.route('/users/edit/<user_id>')
def edit(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s"
    data = {
        'id': user_id
    }
    mysql = connectToMySQL('users')
    user = mysql.query_db(query, data)
    return(render_template('edit.html', user_id = user_id, user=user[0]))

@app.route("/users/edit/<user_id>/update", methods=['POST'])
def update1(user_id):
    query = "UPDATE users SET first_name = %(FN)s, last_name = %(LN)s, email= %(EM)s, updated_at=NOW() WHERE id=%(ID)s"
    data = {
        'FN' : request.form['FN'],
        'LN' : request.form['LN'],
        'EM' : request.form['EM'],
        'ID' : user_id
    }
    print(data)
    test = connectToMySQL('users')
    test.query_db(query, data)
    return redirect('/users')


if __name__ == '__main__':
    app.run(debug=True)