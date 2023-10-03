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

class Subject(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(100))

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, code, name):
        self.code = code
        self.name = name

@app.route('/')
def index():
    _content = '''
    <html>
        
        <body>
            <h1>Heading 1</h1>
            <h3>Heading 3</h3>
            <p>Hello everywa</p>
        </body>
    </html>'''
    return _content

@app.route('/hello/<name>')
def hello(name):
    return "hello "+name+ " :)"

@app.route('/hello/<name>/exams')
def exams(name):
    return "Exams of "+name+ " :)"

@app.route('/hello')
def helloPage():
    name='kenji'
    names=['kenji', 'yascentius']
    return render_template('index.html', name=name, gender='male', names=names)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    resp = make_response(render_template('about.html'))
    # resp.set_cookie('userName', 'Kenji')
    session['userName'] = 'Kenji'
    return resp
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        # Business Logic
        full_name = first_name + ' ' + last_name
        # presentation layer
        return render_template('welcome.html', full_name=full_name, first_name=first_name, last_name=last_name)
    elif request.method == 'GET':
        # first_name = request.args.get('first_name')
        # last_name = request.args.get('last_name')

        # # Business Logic
        # full_name = first_name + ' ' + last_name
        # # presentation layer
        # return render_template('welcome.html', full_name=full_name, first_name=first_name, last_name=last_name)
        return render_template('form.html')
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form_get')
def form_get():
    return render_template('form_get.html')

@app.route('/sayhello')
def sayhello():
    username = session['userName']
    # username = request.cookies.get('userName')
    if username == 'Kenji':
        return render_template('form.html')
    else:
        return render_template('index.html')

@app.route('/addStudent')
def addStudent():
    std1 = Student('Stefanus')
    std2 = Student('Fredrik')
    db.session.add(std1)
    db.session.add(std2)
    db.session.commit()











































































































































































































































Secret_message = "SEPTIO IS GAE FROM BASED FREDRIK"