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
    nim = request.cookies.get('nim')
    if nim:
        return redirect('/home')
    return render_template("log_in.html", log_in = "true")
    

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
                response = make_response(redirect('/staff_home'))
                response.set_cookie('staff_username', staff.username)
                return response
        return render_template("staff_login.html", staff_log_in = "false")
    
@app.route('/home')
def homepage():
    check_denda()
    nim = request.cookies.get('nim')
    if nim:
        user = Student.query.get(nim)
        if user:
            page = int(request.args.get('page', 1))
            books_per_page = 12

            # Read filter and category from query parameters
            filter_text = request.args.get('filter', '')  # Default to an empty string if not provided
            category = request.args.get('category', 'all')  # Default to 'all' for the first visit

            first_visit = not (filter_text or category)

            books = Buku.query

            if filter_text or (category != 'all' and filter_text):
                if category == 'writer':
                    books = books.filter(Buku.author.ilike(f"%{filter_text}%"))
                elif category == 'title':
                    books = books.filter(Buku.nama_buku.ilike(f"%{filter_text}%"))
                elif category == 'genre':
                    books = books.filter(Buku.genre.ilike(f"%{filter_text}%"))

            books = books.all()

            total_pages = (len(books) + books_per_page - 1) // books_per_page
            start_index = (page - 1) * books_per_page
            end_index = start_index + books_per_page

            books_to_display = books[start_index:end_index]

            if not filter_text and (category != 'all' and not request.args.get('filter')) and not first_visit:
                error_message = 'Please Enter a Search Term'
            else:
                error_message = None

            return render_template(
                'home.html',
                books=books_to_display,
                user=user,
                total_buku=len(books),
                halaman=page,
                total_pages=total_pages,
                filter=filter_text,
                category=category,
                error_message=error_message,
            )

    return redirect('/')

# Route ke staff home page
@app.route('/staff_home')
def staff_home():
    check_denda()
    username = request.cookies.get('staff_username')
    if username:
        user_staff = Staff.query.get(username)
        if user_staff:
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
                        'email' : student.email,
                        'batas_pengembalian': denda.batas_pengembalian,
                        'nominal_denda': selisih_hari*1000,
                        'nama_buku': buku.nama_buku,
                        'prodi': student.prodi
                    })
            return render_template('staff_home.html', denda=data_denda)
    return redirect('/staff_login')

@app.route('/peminjaman')
def peminjaman():
    check_denda()
    username = request.cookies.get('staff_username')
    if username:
        user_staff = Staff.query.get(username)
        if user_staff:
            page = int(request.args.get('page', 1))
            books_per_page = 12

            # Read filter and category from query parameters
            filter_text = request.args.get('filter', '')  # Default to an empty string if not provided
            category = request.args.get('category', 'all')  # Default to 'all' for the first visit

            first_visit = not (filter_text or category)

            books = Buku.query

            if filter_text or (category != 'all' and filter_text):
                if category == 'writer':
                    books = books.filter(Buku.author.ilike(f"%{filter_text}%"))
                elif category == 'title':
                    books = books.filter(Buku.nama_buku.ilike(f"%{filter_text}%"))
                elif category == 'genre':
                    books = books.filter(Buku.genre.ilike(f"%{filter_text}%"))

            books = books.all()

            total_pages = (len(books) + books_per_page - 1) // books_per_page
            start_index = (page - 1) * books_per_page
            end_index = start_index + books_per_page

            books_to_display = books[start_index:end_index]

            if not filter_text and (category != 'all' and not request.args.get('filter')) and not first_visit:
                error_message = 'Please Enter a Search Term'
            else:
                error_message = None

            return render_template(
                'peminjaman.html',
                books=books_to_display,
                total_buku=len(books),
                halaman=page,
                total_pages=total_pages,
                filter=filter_text,
                category=category,
                error_message=error_message,
            )
    return redirect('/staff_login')
    
@app.route('/insert_peminjaman', methods=['POST'])
def insert_pinjaman():
    if request.method == "POST":
        id_pinjam = request.form.get('id_peminjaman')
        nim = request.form.get('nim')
        id_buku = request.form.get('book_id')
        keterangan = request.form.get('keterangan')
        tangal_peminjaman = request.form.get('tglPeminjaman')
        batas_pengembalian = request.form.get('tglPengembalian')
        
        peminjaman = Peminjaman(id_pinjam=id_pinjam, nim=nim, id_buku=id_buku ,keterangan=keterangan, tangal_peminjaman=tangal_peminjaman, batas_pengembalian=batas_pengembalian)
        db.session.add(peminjaman)
        buku = Buku.query.filter_by(id_buku=id_buku).first()
        buku.stock -= 1
        db.session.commit()
        return redirect('/staff_home')
    else:
        return "Invalid request."

# Route ke login staff
@app.route('/staff_login')
def staff_login():
    check_denda()
    username = request.cookies.get('staff_username')
    if username:
        return redirect('/staff_home')
    return render_template('staff_login.html')
    

@app.route('/pengembalian')
def pengembalian():
    check_denda()
    username = request.cookies.get('staff_username')
    if username:
        user_staff = Staff.query.get(username)
        if user_staff:
            data_pengembalian = []
            data_query = db.session.query(
                Peminjaman, Buku
            ).join(
                Buku, Peminjaman.id_buku == Buku.id_buku
            ).filter(Peminjaman.keterangan == "BELUM KEMBALI").all()
            for peminjaman, buku in data_query:
                data_pengembalian.append({
                    'nim': peminjaman.nim,
                    'id_buku': peminjaman.id_buku,
                    'nama_buku': buku.nama_buku,
                    'batas_pengembalian': peminjaman.batas_pengembalian,
                    'id_pinjam': peminjaman.id_pinjam,

                })
            return render_template('pengembalian.html', data_pengembalian=data_pengembalian)
    return redirect('/staff_login')

@app.route('/registration')
def registration():
    check_denda()
    username = request.cookies.get('staff_username')
    if username:
        user_staff = Staff.query.get(username)
        if user_staff:

            return render_template('registration.html')
    return redirect('/staff_login')

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
    
@app.route('/update_peminjaman', methods=["POST"])
def update_peminjaman():
   id_pinjam = request.args.get('id_pinjam')
   peminjaman_record = Peminjaman.query.filter_by(id_pinjam=id_pinjam).first()
   if peminjaman_record:
        peminjaman_record.keterangan = "KEMBALI"
        buku = Buku.query.filter_by(id_buku=peminjaman_record.id_buku).first()
        buku.stock += 1
        db.session.commit()

        return "Success"
   return "Failed to update Peminjaman record."

@app.route('/update_denda', methods=["POST"])
def update_denda():
    id_denda = request.args.get('id_denda')
    denda_record = Denda.query.filter_by(id_denda=id_denda).first()
    if denda_record:
            denda_record.status = "LUNAS"
            db.session.commit()

            return "Success"
    return "Failed to update Peminjaman record."

if __name__ == '__main__':
    app.run(debug=True)