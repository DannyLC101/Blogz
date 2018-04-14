from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'
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
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

        blogs = Blog.query.filter_by(title=blog_title).all()
        #blog_text = Blog.query.all()
        return render_template('blog.html', blogs=blogs)
    else:
        return render_template('newpost.html')

@app.route('/blog', methods=['GET','POST'])
def main_blog():
    #if request.method=='POST':
    #    blog_id = int(request.form['blog-id'])
    #    blogs = Blog.query.get(blog_id)
    #    return render_template('blog.html', blogs=blogs)
    #elif request.method=='GET':
    #    blog_id = int(request.form['blog-id'])
    #    blogs = Blog.query.get(blog_id)
    #    return redirect('/blog?id='+blog_id,blogs=blogs)
    blog_id = request.args.get('title')
    blogs = Blog.query.filter_by(id=blog_id).first()
    return render_template('blog.html', blogs=blogs)

@app.route('/blog?id=', methods=['GET', 'POST'])
def blog():
    id_blogs = request.args.get(blog-id)
    blogs = Blog.request.get(id_blogs)
    return render_template('blog.html', blogs=blogs)

@app.route('/', methods=['POST', 'GET'])
def index():
    #if request.method=='GET':
     #   blog_id = request.args.get('blog-id')
     #   blogs = Blog.query.filter_by(blog_id).first()
      #  return render_template('blog.html', blogs=blogs)
    
    blogs = Blog.query.filter_by().all()
    return render_template('index.html', blogs=blogs)

if __name__=='__main__':
    app.run()        
