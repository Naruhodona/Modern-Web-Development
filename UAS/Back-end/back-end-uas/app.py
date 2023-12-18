from flask import Flask, render_template, request, make_response, session, redirect, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import base64
from collections import defaultdict

app = Flask(__name__)
CORS(app)

app.secret_key = 'UASWeb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/restoran'
app.config['SQLALCHEMT_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model untuk tabel Admin
class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Model untuk tabel Meja
class Meja(db.Model):
    no_meja = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=True)

# Model untuk tabel Menu
class Menu(db.Model):
    id_menu = db.Column(db.String(11), primary_key=True)
    nama_menu = db.Column(db.String(255), nullable=True)
    harga = db.Column(db.Integer, nullable=True)
    tipe = db.Column(db.String(255), nullable=True)
    gambar = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, id_menu, nama_menu, harga, tipe, gambar):
        self.id_menu = id_menu
        self.nama_menu = nama_menu
        self.harga = harga
        self.tipe = tipe
        self.gambar = gambar

# Model untuk tabel Order
class Order(db.Model):
    kode_order = db.Column(db.String(100), primary_key=True)
    order_id = db.Column(db.String(100))
    status_order = db.Column(db.String(255))
    id_menu = db.Column(db.String(11))
    no_meja = db.Column(db.Integer)
    nama_reservasi = db.Column(db.String(255))

# Pengambilan data dalam bentuk JSON untuk Admin
@app.route('/admin-login', methods=['POST'])
def login():
    data = request.json 
    username = data.get('username')

    admin = Admin.query.filter_by(username=username).first()

    if admin:
        admin_data = {
            'id_admin': admin.id_admin,
            'username': admin.username,
            'password': admin.password
        }
        return jsonify({'admin': admin_data}), 200
    else:
        return jsonify({'message': 'Admin not found'}), 404

@app.route('/menu', methods=['POST', 'GET'])
def menu():
    if request.method == 'GET':
        try:
            menus = Menu.query.all()

            menu_list = []
            for menu in menus:
                menu_data = {
                    'id_menu': menu.id_menu,
                    'nama_menu': menu.nama_menu,
                    'harga': menu.harga,
                    'tipe': menu.tipe
                }

                if menu.gambar:
                    image_base64 = base64.b64encode(menu.gambar).decode('utf-8')
                    menu_data['image_base64'] = f"data:image/jpeg;base64,{image_base64}"

                menu_list.append(menu_data)

            return jsonify({'menus': menu_list}), 200

        except Exception as e:
            return jsonify({'message': str(e)}), 500
        
    elif request.method == 'POST':
        try:
            data = request.json
                        
            namaMenu = data['namaMenu']
            hargaMenu = int(data['hargaMenu'])
            tipeMenu = data['tipeMenu']
            
            # Ambil gambar dari data JSON sebagai string Base64
            gambarMenu_base64 = data['gambarMenu']

            # Konversi gambar dari Base64 ke bentuk binary
            gambarMenu = base64.b64decode(gambarMenu_base64)
            jumlah_menu = Menu.query.filter_by(tipe=tipeMenu).count()
            
            if tipeMenu == 'Minuman':
                id_menu = 'B' + str(jumlah_menu + 1)
            else:
                id_menu = 'F' + str(jumlah_menu + 1)

            menu = Menu(
                id_menu=id_menu,
                nama_menu=namaMenu,
                harga=hargaMenu,
                tipe=tipeMenu,
                gambar=gambarMenu 
            )
            db.session.add(menu)
            db.session.commit()

            return jsonify({'message': 'Menu inserted successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500

# Route mengambil daftar Menu berdasarkan id nya lalu dapat melakukan edit dan delete
@app.route('/menu/<id_menu>', methods=['GET', 'PUT', 'DELETE'])
def selected_menu(id_menu):
    if request.method == 'GET':
        try:
            menu = Menu.query.filter_by(id_menu=id_menu).first()

            if menu:
                # Mengubah data gambar BLOB ke format base64
                if menu.gambar:
                    image_base64 = base64.b64encode(menu.gambar).decode('utf-8')
                    menu.image_base64 = f"data:image/jpeg;base64,{image_base64}"

                return jsonify({
                    'id_menu': menu.id_menu,
                    'nama_menu': menu.nama_menu,
                    'harga': menu.harga,
                    'tipe': menu.tipe,
                    'gambar': menu.image_base64 if menu.gambar else None
                }), 200
            else:
                return jsonify({'message': 'Menu not found'}), 404
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        
    elif request.method == 'PUT':
        try:
            data = request.json

            menu = Menu.query.filter_by(id_menu=id_menu).first()

            if menu:
                menu.nama_menu = data.get('nama_menu', menu.nama_menu)  # Perbaikan nama field
                menu.harga = int(data.get('harga', menu.harga))  # Perbaikan nama field
                menu.tipe = data.get('tipe', menu.tipe)  # Perbaikan nama field

                # Update gambar jika ada perubahan
                if data['gambar']:
                    gambarMenu_base64 = data['gambar']
                    gambarMenu = base64.b64decode(gambarMenu_base64)
                    menu.gambar = gambarMenu

                db.session.commit()

                return jsonify({'message': 'Menu updated successfully'}), 200
            else:
                return jsonify({'message': 'Menu not found'}), 404

        except Exception as e:
            return jsonify({'message': str(e)}), 500
        
    elif request.method == 'DELETE':
        try:
            menu = Menu.query.filter_by(id_menu=id_menu).first()

            if menu:
                db.session.delete(menu)
                db.session.commit()
                return jsonify({'message': 'Menu deleted successfully'}), 200
            else:
                return jsonify({'message': 'Menu not found'}), 404
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'Method not allowed'}), 405

# Testing
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        all_orders = db.session.query(Order).all()

        orders_with_details = []

        for order in all_orders:
            meja_info = Meja.query.filter_by(no_meja=order.no_meja).first()

            menu_info = Menu.query.filter_by(id_menu=order.id_menu).first()

            order_details = {
                'kode_order': order.kode_order,
                'order_id': order.order_id,
                'status_order': order.status_order,
                'id_menu': order.id_menu,
                'no_meja': order.no_meja,
                'nama_reservasi': order.nama_reservasi,
                'meja_status': meja_info.status if meja_info else None,
                'menu_nama': menu_info.nama_menu if menu_info else None
            }
            orders_with_details.append(order_details)

        menus = Menu.query.all()

        available_tables = Meja.query.filter_by(status='AVAILABLE').all()
        available_menu_names = [menu.nama_menu for menu in menus]
        available_table_numbers = [table.no_meja for table in available_tables]

        data = {
            "menu_names": available_menu_names,
            "table_numbers": available_table_numbers,
            "orders_with_details": orders_with_details
        }

        return jsonify(data)
    
    elif request.method == 'POST':
        data = request.get_json()
        order_id = data.get('order_id')
        nama_reservasi = data.get('reservasi')
        nomor_meja = data.get('tables')
        status_order = data.get('status_order')
        menu_selected = data.get('selected_menu[]')
   
        meja = Meja.query.filter_by(no_meja=nomor_meja).first()
       
        if not isinstance(menu_selected, list):
            menu_selected = [menu_selected]
        if meja:
            meja.status = 'OCCUPIED'

        count_orders = Order.query.count()
        kode_order = Order.query.count()
        menus = Menu.query.filter(Menu.nama_menu.in_(menu_selected)).all()
    
        # if not menus:
        #     return jsonify({'error': 'Menus not found'}), 404
   
        id_menus = [menu.id_menu for menu in menus]

        if order_id:
            for id_menu in id_menus:
                new_order = Order(
                    kode_order = kode_order,
                    order_id=order_id,
                    status_order=status_order,
                    id_menu=id_menu,
                    no_meja=nomor_meja,
                    nama_reservasi=nama_reservasi
                )
                db.session.add(new_order)
                kode_order += 1
            
            db.session.commit()
            response_data = {
                'message': 'Order submitted successfully',
                'nama_reservasi': nama_reservasi,
                'nomor_meja': nomor_meja,
                'status_order': status_order,
                'selected_menu': menu_selected,
                'order_id': order_id
            }
            return jsonify(response_data)
        else:
        
            new_id_order = ''
            print(id_menus, "kadawjd")
            for id_menu in id_menus:
                
                new_id_order = f"ORD-{count_orders + 1}"
                new_order = Order(
                    kode_order = kode_order,
                    order_id=new_id_order,
                    status_order=status_order,
                    id_menu=id_menu,
                    no_meja=nomor_meja,
                    nama_reservasi=nama_reservasi
                )
                db.session.add(new_order)
                kode_order += 1
            print("commit")
            db.session.commit() 
           
            response_data = {
                'message': 'Order submitted successfully',
                'nama_reservasi': nama_reservasi,
                'nomor_meja': nomor_meja,
                'status_order': status_order,
                'selected_menu': menu_selected,
                'order_id': new_id_order
            }
            print(response_data)
            return jsonify(response_data)

@app.route('/order/<string:order_id>', methods=['GET', 'PUT', 'POST'])
def selected_order(order_id):
    if request.method == 'GET':
        orders = Order.query.filter_by(order_id=order_id).all()

        orders_details = []

        for order in orders:
            order_detail = {
                'kode_order': order.kode_order,
                'order_id': order.order_id,
                'status_order': order.status_order,
                'no_meja': order.no_meja,
                'nama_reservasi': order.nama_reservasi,
                'id_menu': order.id_menu 
            }
            orders_details.append(order_detail)

        return jsonify(orders_details)

    elif request.method == 'PUT':
        data = request.get_json()
        # kode_order = data.get('kode_order')
        no_meja = data.get('no_meja')

        # if kode_order:
        updated_orders = Order.query.filter_by(order_id=order_id).all()
        for order in updated_orders:
            order.status_order = "Tertutup"

        if no_meja:
            meja = Meja.query.filter_by(no_meja=no_meja).first()
            if meja:
                meja.status = "AVAILABLE"

        db.session.commit()
        return jsonify({'message': 'Order status and Meja status updated successfully',
                        'Meja status': meja.status if meja else None})

    if request.method == 'POST':
        data = request.get_json()
        order_id = data[0].get('order_id')
        kode_order = data[0].get('kode_order')
        nama_reservasi = data[0].get('nama_reservasi')
        nomor_meja = data[0].get('no_meja')
        status_order = data[0].get('status_order')
        menu_selected = data[0].get('id_menu')
        menus = Menu.query.filter(Menu.nama_menu.in_(menu_selected)).all()
        id_menus = [menu.id_menu for menu in menus]

        if status_order == "Terbuka":
            for id_menu in id_menus:
                new_order = Order(
                    kode_order = kode_order,
                    order_id= order_id,
                    status_order=status_order,
                    id_menu=id_menu,
                    no_meja=nomor_meja,
                    nama_reservasi=nama_reservasi
                )
                db.session.add(new_order)
     
            db.session.commit() 
            response_data = {
                'message': 'Order submitted successfully',
            }

            return jsonify(response_data)
  
# Route mengambil seluruh meja
@app.route('/meja', methods=['GET'])
def meja():
    all_meja = Meja.query.all()

    if not all_meja:
        return jsonify({'message': 'Tidak ada meja yang tersedia'}), 404

    meja_list = []  

    for meja in all_meja:
        meja_data = {
            'no_meja': meja.no_meja,
            'status': meja.status
        }
        meja_list.append(meja_data)

    return jsonify({'meja': meja_list})

# Route mengambil meja berdasarkan no_meja beserta mengubah statusnya
@app.route('/meja/<int:no_meja>', methods=['GET', 'PUT'])
def selected_meja(no_meja):
    meja = Meja.query.filter_by(no_meja=no_meja).first()

    if not meja:
        return jsonify({'message': 'Meja tidak ditemukan'}), 404

    if request.method == 'GET':
        meja_data = {
            'no_meja': meja.no_meja,
            'status': meja.status
        }
        return jsonify({'meja': meja_data})

    elif request.method == 'PUT':
        new_status = request.json.get('status')

        if new_status is None:
            return jsonify({'message': 'Data status tidak lengkap'}), 400

        meja.status = new_status
        db.session.commit()

        return jsonify({'message': 'Status meja berhasil diubah'})

if __name__ == '__main__':
    app.run(debug=True)