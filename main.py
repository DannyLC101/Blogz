from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method=='POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_title = Blog(blog_title)
        new_body = Blog(blog_body)
        db.session.add(new_title)
        db.session.add(new_body)
        db.session.commit()

        blogs = Blog.query.all()
        #blog_text = Blog.query.all()
        return render_template('index.html', blogs=blogs)
    else:
        return render_template('newpost.html')

#@app.route('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    #if request.method=='POST':
     #   blog_title = request.form['']
     return render_template('index.html')

if __name__=='__main__':
    app.run()        
