from flask import Flask, render_template, request , redirect, flash,url_for,session
from flask_sqlalchemy import SQLAlchemy
import datetime
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)
app.secret_key = 'Gautami'

class User(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(300), unique=True)
    date_joined=db.Column(db.Date, default=datetime.datetime.utcnow())
    password= db.Column(db.String(50), nullable=False)
    relation = db.relationship('Blog', backref='user', lazy=True)

    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    
class Blog(db.Model):
    blog_id =db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(400),nullable=False)
    blog=db.Column(db.Text,nullable=False)
    time=db.Column(db.Date, default=datetime.datetime.now())
    user_id= db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __init__(self,title,blog,user_id):
        self.title=title
        self.blog=blog
        self.user_id=user_id


with app.app_context():
    db.create_all()

def is_logged_in():
    return 'logged_in' in session

def get_logged_in_user():
    if 'logged_in' in session and 'email' in session:
        return{ 'email': session['email'], 'name': session['name']}
    return None

# Use a context processor to pass logged_in status to all templates:
# Add a context processor to pass the logged_in status to all templates.
@app.context_processor
def inject_user():
    return dict(logged_in=is_logged_in(),user=get_logged_in_user())


@app.route("/", methods=['GET','POST'] )
def hello_world():
    # return render_template('index.html', logged_in = is_logged_in())
    return render_template('index.html')
@app.route("/home", methods=['GET','POST'] )
def home():
    return render_template('home.html')

@app.route("/dashboard", methods=['GET','POST'] )
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile',methods=['GET','POST'])
def profile():
    return render_template('profile.html')

@app.route('/read', methods=['GET','POST'])
def read():
    data =User.query.all()
    if request.method == 'POST':
        user_id= request.form.get('update')
        if user_id :
            return redirect(url_for('update',user_id=user_id))
    return render_template('read.html', data=data)

@app.route('/update',methods=['GET','POST'])
def update():
    user_id= request.args.get('user_id')
    user= User.query.filter_by(user_id=user_id).first()
    if not user :
        flash("user not found", 'danger')
        return redirect(url_for('read'))
    if request.method=='POST':
        user_name=request.form['update_name']
        user_email=request.form['update_email']
        user_password= request.form['update_password']
        hashed_password=bcrypt.hashpw(user_password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

        user.name=user_name
        user.email=user_email
        user.password=hashed_password
        db.session.commit()
        flash("User details updated successfully",'success')
    return render_template('update.html',user=user)

@app.route('/delete',methods=['GET','POST'])
def delete():
    user_id=request.form.get('delete')
    if request.method =='POST':
        # User model has user_id column then check the first value of that user_id
        user= User.query.filter_by(user_id = user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted successfully", 'danger')
        return redirect("read")
    return 'delete'

# create
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name= request.form['name']
        email= request.form['email']
        password= request.form['password']

        user = User(name=name, email=email, password= password)
        db.session.add(user)
        db.session.commit()
        flash("User created successfully !!" , "success")
        # return redirect('login')

    else:
        flash("Please try with different email", "danger")

    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if email and  user.check_password(password):
            session['email']=user.email
            # session['password']=user.password
            session['name']=user.name

            session['logged_in']=True

            flash("User logged in successfully", 'success')     
        else:
            flash("Invalid credentials",'danger')         
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash("user logged out !", 'danger')
    return redirect('login')

if __name__ == '__main__':
    app.run(debug=True)
