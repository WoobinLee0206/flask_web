from flask import Flask ,render_template, flash, redirect, url_for, session, request, logging
from data import Articles
import pymysql
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.debug=True

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='myflaskapp')


@app.route('/')
def index():
    print("Success")
    # return "TEST"
    return render_template('home.html',hello="GaryKim")

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('email')
        pw = request.form.get('password')
        # print([id , pw])

        sql='SELECT * FROM users WHERE email = %s'
        cursor  = db.cursor()
        cursor.execute(sql, [id])
        users = cursor.fetchone()
        print(users)

        if users == None:
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(pw, users[4]):
                return redirect(url_for('articles'))
            else:
                return redirect(url_for('login'))
        
        # return "Success"
    else:
        return render_template('login.html')



@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # data = request.body.get('author')
        name = request.form.get('name')
        email = request.form.get('email')
        password = pbkdf2_sha256.hash(request.form.get('password'))
        re_password = request.form.get('re_password')
        username = request.form.get('username')
        # name = form.name.data

        if(pbkdf2_sha256.verify(re_password, password)):
            print(pbkdf2_sha256.verify(re_password, password))
            cursor = db.cursor()
            sql = '''
                INSERT INTO users (name, email, username, password) 
                VALUES (%s ,%s, %s, %s)
             '''
            cursor.execute(sql, (name, email, username, password))
            db.commit()
            # cursor = db.cursor()
            # cursor.execute('SELECT * FROM users;')
            # users = cursor.fetchall()

            return redirect(url_for('login'))
        else:
            return "Invalid Password"
        
        db.close()
    else:
        return render_template('register.html')



@app.route('/about')
def about():
    print("Success")
    # return "TEST"
    return render_template('about.html',hello="GaryKim")

@app.route('/articles')
def articles():
    # articles = Articles()
    # print(len(articles))
    cursor = db.cursor()
    sql = 'SELECT * FROM topic;'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return render_template('articles.html', articles = data)


@app.route('/article/<int:id>')
def article(id):
    print(type(id))
    articles= Articles()[id-1]
    # print(articles)
    return render_template('article.html',data = articles)
    # return "Success"

@app.route('/add_articles', methods = ['GET', 'POST'])
def add_articles():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        author = request.form['author']
        cursor = db.cursor()
        sql = ''' 
        INSERT INTO topic (title, body, author) 
                VALUES (%s ,%s, %s)
        '''
        cursor.execute(sql, (title, body, author))
        db.commit()
        return redirect("/articles")
    else:
        return render_template('add_articles.html')
    db.close()



if __name__ =='__main__':
    # app.run(host='0.0.0.0', port='8080')
    app.run()