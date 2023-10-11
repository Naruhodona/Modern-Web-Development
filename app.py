from flask import Flask, render_template, request, make_response, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'UTSWeb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/uts_pwm'
app.config['SQLALCHEMT_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'student'
    nim = db.Column(db.String(9), primary_key = True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100))
    prodi = db.Column(db.String(100))
    password = db.Column(db.String(20))

    denda = db.relationship('Denda', backref='denda')
    peminjaman = db.relationship("Peminjaman", backref='peminjaman')

    def __init__(self, nim, nama, email, prodi, password):
        self.nim = nim
        self.nama = nama
        self.email = email
        self.prodi = prodi
        self.password = password

class Buku(db.Model):
    __tablename__ = 'buku'
    id_buku = db.Column(db.String(100), primary_key=True)
    nama_buku = db.Column(db.Text)
    author = db.Column(db.Text)
    genre = db.Column(db.Text)
    stock = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.Text)
    # denda = db.relationship('Denda', backref='denda')
    # peminjaman = db.relationship("Peminjaman", backref='peminjaman')

    def __init__(self, id_buku, nama_buku, author, genre, stock, description, image):
        self.id_buku = id_buku
        self.nama_buku = nama_buku
        self.author = author
        self.genre = genre
        self.stock = stock
        self.description = description
        self.image = image

class Staff(db.Model):
    __tablename__ = 'staff'
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Peminjaman(db.Model):
    __tablename__ = 'peminjaman'
    id_pinjam = db.Column(db.String(100), primary_key=True)
    nim = db.Column(db.String(9), db.ForeignKey('student.nim'))
    id_buku = db.Column(db.String(9), db.ForeignKey('buku.id_buku'))
    keterangan = db.Column(db.Text)
    batas_pengembalian = db.Column(db.Date)
    tangal_peminjaman = db.Column(db.Date)
    
    def __init__(self, id_pinjam, nim, id_buku, keterangan, batas_pengembalian, tangal_peminjaman):
        self.id_pinjam = id_pinjam
        self.nim = nim
        self.id_buku = id_buku
        self.keterangan = keterangan
        self.batas_pengembalian = batas_pengembalian
        self.tangal_peminjaman = tangal_peminjaman

class Denda(db.Model):
    __tablename__ = 'denda'
    id_denda = db.Column(db.String(100), primary_key=True)
    nim = db.Column(db.String(9), db.ForeignKey('student.nim'))
    id_buku = db.Column(db.String(9), db.ForeignKey('buku.id_buku'))
    batas_pengembalian = db.Column(db.Date)
    nominal_denda = db.Column(db.Integer)

    def __init__(self, id_denda, nim, id_buku, batas_pengembalian, nominal_denda):
        self.id_denda = id_denda
        self.nim = nim
        self.id_buku = id_buku
        self.batas_pengembalian = batas_pengembalian
        self.nominal_denda = nominal_denda

@app.route('/')
def index():
    return render_template("log_in.html", log_in = "true")

# Route untuk registration
@app.route('/registration')
def registration():
    return render_template('registration.html')

# Route ke profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        nim = request.form.get('NIM')
        password = request.form.get('password')
        
        students = Student.query.all()
        
        for student in students:
            if student.nim == nim and student.password == password:
                return redirect('/home')
        return render_template("log_in.html", log_in = "false")
    
@app.route('/staff-login', methods=['POST'])
def login_staff():
    if request.method == "POST":
        username = request.form.get('Username')
        password = request.form.get('password')
        
        staffs = Staff.query.all()
        
        for staff in staffs:
            if staff.username == username and staff.password == password:
                return render_template('staff_home.html')
        return render_template("staff_login.html", staff_log_in = "false")
    
@app.route('/insert_peminjaman', methods=['POST'])
def insert_pinjaman():
    if request.method == "POST":
        id_pinjam = request.form.get('id_peminjaman')
        nim = request.form.get('nim')
        id_buku = request.form.get('id_buku')
        keterangan = request.form.get('keterangan')
        tangal_peminjaman = request.form.get('tglPeminjaman')
        batas_pengembalian = request.form.get('tglPengembalian')
        print(id_buku)
        peminjaman = Peminjaman(id_pinjam=id_pinjam, nim=nim, id_buku=id_buku ,keterangan=keterangan, tangal_peminjaman=tangal_peminjaman, batas_pengembalian=batas_pengembalian)
        db.session.add(peminjaman)
        db.session.commit()

        return redirect('/staff_home')
    else:
        return "Invalid request."

# Route ke home
@app.route('/home')
def homepage():
    books = Buku.query.all()
    return render_template('home.html', books=books)

@app.route('/peminjaman')
def peminjaman():
    books = Buku.query.all()
    return render_template("peminjaman.html", books=books)



# Route ke staff home page
@app.route('/staff_home')
def staff_home():
    return render_template('staff_home.html')

# Route ke login staff
@app.route('/staff_login')
def staff_login():
    return render_template('staff_login.html')

@app.route('/peminjaman')
def pinjam():
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