from flask import Flask, render_template, request, make_response, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'skip2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/mwd_2023'
app.config['SQLALCHEMT_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(200))

    subjects = db.relationship('Subject', backref='subject')

    def __init__(self, name):
        self.name = name

# class Subject(db.Model):
#     id = db.Column('id', db.Integer, primary_key=True)
#     code = db.Column(db.String(50))
#     name = db.Column(db.String(100))

#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

#     def __init__(self, code, name):
#         self.code = code
#         self.name = name

@app.route('/')
def index():
    return render_template('log_in.html')

# @app.route('/hello/<name>')
# def hello(name):
#     return "hello "+name+ " :)"

# @app.route('/hello/<name>/exams')
# def exams(name):
#     return "Exams of "+name+ " :)"

# @app.route('/hello')
# def helloPage():
#     name='kenji'
#     names=['kenji', 'yascentius']
#     return render_template('index.html', name=name, gender='male', names=names)

# # Route untuk log in
# @app.route('/log_in')
# def log_in():
#     return render_template('log_in.html')

# Route untuk registration
@app.route('/registration')
def registration():
    return render_template('registration.html')

# Route ke profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Route ke home
@app.route('/home')
def home():
    return render_template('home.html')

# Route ke staff home page
@app.route('/staff_home')
def staff_home():
    return render_template('staff_home.html')

# Route ke login staff
@app.route('/staff_login')
def staff_login():
    return render_template('staff_login.html')

@app.route('/peminjaman')
def peminjaman():
    return render_template('peminjaman.html')

@app.route('/pengembalian')
def pengembalian():
    return render_template('pengembalian.html')
# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     resp = make_response(render_template('about.html'))
#     # resp.set_cookie('userName', 'Kenji')
#     session['userName'] = 'Kenji'
#     return resp
#     if request.method == 'POST':
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         # Business Logic
#         full_name = first_name + ' ' + last_name
#         # presentation layer
#         return render_template('welcome.html', full_name=full_name, first_name=first_name, last_name=last_name)
#     elif request.method == 'GET':
#         # first_name = request.args.get('first_name')
#         # last_name = request.args.get('last_name')

#         # # Business Logic
#         # full_name = first_name + ' ' + last_name
#         # # presentation layer
#         # return render_template('welcome.html', full_name=full_name, first_name=first_name, last_name=last_name)
#         return render_template('form.html')
# @app.route('/form')
# def form():
#     return render_template('form.html')

# @app.route('/form_get')
# def form_get():
#     return render_template('form_get.html')

# @app.route('/sayhello')
# def sayhello():
#     username = session['userName']
#     # username = request.cookies.get('userName')
#     if username == 'Kenji':
#         return render_template('form.html')
#     else:
#         return render_template('index.html')

# @app.route('/addStudent')
# def addStudent():
#     std1 = Student('Stefanus')
#     std2 = Student('Fredrik')
#     db.session.add(std1)
#     db.session.add(std2)
#     db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)