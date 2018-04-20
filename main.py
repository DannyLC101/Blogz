from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'
db = SQLAlchemy(app)

class Blogz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(30))
    blogs = db.relationship('Blogz', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("<'username'> Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or does not exist', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            return "<h1>Username already exist</h1>"
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
        
    if request.method=='POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if blog_title=="" and  blog_body=="":
            error1 = "please enter the title"
            error2 = "please enter the body"
            return render_template('newpost.html', error1=error1, error2=error2)
        if blog_title=="":
            error1 = "please enter the title"
            return render_template('newpost.html', error1=error1, body=blog_body)
        if blog_body=="":
            error2 = "please enter the body"
            return render_template('newpost.html', title=blog_title, error2=error2)
        
        else:

            new_blog = Blogz(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            blogs = Blogz.query.filter_by(title=blog_title).all()
            #blog_text = Blog.query.all()
            return render_template('blog.html', blogs=blogs)
    else:
        return render_template('newpost.html')



@app.route('/', methods=['POST', 'GET'])
def index():
    #if request.method=='GET':
     #   blog_id = request.args.get('blog-id')
     #   blogs = Blog.query.filter_by(blog_id).first()
      #  return render_template('blog.html', blogs=blogs)
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blogz(blog_title, blog_body, owner)
        db.session.add(new_blog)
        db.session.commit()

        blogs = Blogz.query.filter_by(owner=owner).all()
        return render_template('index.html', blogs=blogs)

    blogs = Blogz.query.filter_by().all()
    return render_template('index.html', blogs=blogs)

@app.route('/blog', methods=['GET'])
def main_blog():
    #if request.method=='POST':
    #    blog_id = int(request.form['blog-id'])
    #    blogs = Blog.query.get(blog_id)
    #    return render_template('blog.html', blogs=blogs)
    #elif request.method=='GET':
    #    blog_id = int(request.form['blog-id'])
    #    blogs = Blog.query.get(blog_id)
    #    return redirect('/blog?id='+blog_id,blogs=blogs)
    blog_id = request.args.get('id')
    blogs = Blogz.query.filter_by(id=blog_id)
    return render_template('blog.html', blogs=blogs)

#@app.route('/blog?id=', methods=['GET'])
#def blog():
#    id_blogs = request.form['blog-id']
 #   blogs = Blog.query.filter_by(id=id_blogs)
  #  return render_template('blog.html', blogs=blogs)


if __name__=='__main__':
    app.run()        
