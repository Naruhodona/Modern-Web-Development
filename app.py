from flask import Flask, render_template, request, make_response, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    status = db.Column(db.Text)

    def __init__(self, id_denda, nim, id_buku, batas_pengembalian, status):
        self.id_denda = id_denda
        self.nim = nim
        self.id_buku = id_buku
        self.batas_pengembalian = batas_pengembalian
        self.status = status

def check_denda():
    today = datetime.now()
    data_denda = Denda.query.all()
    list_id_denda = []
    for dd in data_denda:
        list_id_denda.append(dd.id_denda)
    joined_data = db.session.query(Peminjaman, Student).join(Student, Peminjaman.nim == Student.nim).all()
    status_list = []
    for peminjaman, student in joined_data:
        due_date = datetime.strptime(str(peminjaman.batas_pengembalian), '%Y-%m-%d')
        if (today - due_date).days > 0:
            try:
                for dd in data_denda:
                    if (peminjaman.nim == dd.nim) and (peminjaman.id_buku == dd.id_buku):
                        if dd.status == "LUNAS":
                            status_list.append(True)
                        else:
                            status_list.append(False)
                    else:
                        id_denda = "D" + str(due_date.year) + str(due_date.month) + str(due_date.day) + str(peminjaman.nim) + str(peminjaman.id_buku)
                        if id_denda not in list_id_denda:
                            denda = Denda(id_denda=id_denda, nim=peminjaman.nim, id_buku=peminjaman.id_buku ,status="BELUM LUNAS", batas_pengembalian=peminjaman.batas_pengembalian)
                            db.session.add(denda)
                            db.session.commit()
                            
                if False not in status_list and status_list != []:
                    id_denda = "D" + str(due_date.year) + str(due_date.month) + str(due_date.day) + str(peminjaman.nim) + str(peminjaman.id_buku)
                    if id_denda not in list_id_denda:
                        denda = Denda(id_denda=id_denda, nim=peminjaman.nim, id_buku=peminjaman.id_buku ,status="BELUM LUNAS", batas_pengembalian=peminjaman.batas_pengembalian)
                        db.session.add(denda)
                        db.session.commit()
                status_list = []
            except Exception as e:
                print("Kesalahan", str(e))
                db.session.rollback()

@app.route('/')
def index():
    check_denda()
    return render_template("log_in.html", log_in = "true")

# Route untuk registration
@app.route('/registration')
def registration():
    check_denda()
    return render_template('registration.html')

# Route ke profile page
@app.route('/profile')
def profile():
    check_denda()
    nim = request.cookies.get('nim')
    if nim:
        # Lakukan sesuatu dengan user_id, seperti mengambil data pengguna
        user = Student.query.get(nim)
        if user:
            joined_data = db.session.query(Denda, Buku, Student).join(Buku, Denda.id_buku == Buku.id_buku).join(Student, Denda.nim == Student.nim).all()
            data_user = Student.query.filter(Student.nim == nim)
            data_denda = []
            for denda, buku, student in joined_data:
                today = datetime.now()
                selisih_hari = (today - datetime.strptime(str(denda.batas_pengembalian), '%Y-%m-%d')).days
                if denda.status !=  "LUNAS" and denda.nim == nim:
                    data_denda.append({
                        'id_denda': denda.id_denda,
                        'id_buku': denda.id_buku,
                        'batas_pengembalian': denda.batas_pengembalian,
                        'nominal_denda': "Rp. "+str(selisih_hari*1000),
                        'nama_buku': buku.nama_buku
                    })
            return render_template('profile.html', data_user=data_user, data_denda=data_denda)
    else:
        return redirect('/')
    

@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        nim = request.form.get('NIM')
        password = request.form.get('password')
        
        students = Student.query.all()
        
        for student in students:
            if student.nim == nim and student.password == password:
                response = make_response(redirect('/home'))
                response.set_cookie('nim', student.nim)
                return response
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
        id_buku = request.form.get('book_id')
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
    nim = request.cookies.get('nim')
    if nim:
        # Lakukan sesuatu dengan user_id, seperti mengambil data pengguna
        user = Student.query.get(nim)
        if user:
            # Pengguna sudah login, tampilkan halaman /home
            books = Buku.query.all()
            return render_template('home.html', books=books, user=user)
    # Pengguna belum login, mungkin Anda ingin mengarahkan mereka kembali ke halaman login
    return redirect('/')

@app.route('/peminjaman')
def peminjaman():
    books = Buku.query.all()
    return render_template("peminjaman.html", books=books)

# Route ke staff home page
@app.route('/staff_home')
def staff_home():
    joined_data = db.session.query(Denda, Buku, Student).join(Buku, Denda.id_buku == Buku.id_buku).join(Student, Denda.nim == Student.nim).all()
    data_denda = []
    for denda, buku, student in joined_data:
        today = datetime.now()
        selisih_hari = (today - datetime.strptime(str(denda.batas_pengembalian), '%Y-%m-%d')).days
        if denda.status !=  "LUNAS":
            data_denda.append({
                'id_denda': denda.id_denda,
                'nim': denda.nim,
                'nama': student.nama,
                'id_buku': denda.id_buku,
                'batas_pengembalian': denda.batas_pengembalian,
                'nominal_denda': selisih_hari*1000,
                'nama_buku': buku.nama_buku,
                'prodi': student.prodi
            })
    return render_template('staff_home.html', denda=data_denda)

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

@app.route('/insert_registration', methods=["POST"])
def insert_registration():
    if request.method == "POST":
        nim = request.form.get('NIM')
        nama = request.form.get('nama')
        email = request.form.get('email')
        password = request.form.get('password')
        prodi = request.form.get('prodi')
        student = Student(nim=nim, nama=nama ,email=email, password=password, prodi=prodi)
        db.session.add(student)
        db.session.commit()

    return redirect('/staff_home')
    


if __name__ == '__main__':
    app.run(debug=True)