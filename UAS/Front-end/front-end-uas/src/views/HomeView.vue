<template>
<html>
  <head>
  <title>Homepage Restoran</title>

  </head>
  <body>
    <header>
      <!-- Header -->
      <div class="header">
        <div class="header-inner">
          <h1>Selamat Datang di Restoran Triwahyudi</h1>
          Silakan pilih nomor meja Anda:
        </div>
        
      </div>
    </header>

    <main>
      <!-- Content -->
      <div class="container">
        <div class="row">
          <!-- Nomor Meja -->
          <div v-for="table in tables" :key="table.no_meja" class="col-md-3">
            <div :class="getTableStatusClass(table.status)" :id="table.no_meja" @click="chooseTable(table.no_meja)">
              <h3>Table <br> {{ table.no_meja }}</h3>
            </div> 
          </div>
          <div class="info">
            <div style="background-color: red; width: 50px; height: 50px; margin: 10px"></div><span style="align-self: center; margin: 10px">OCCUPIED</span>
            <div style="background-color: lightgrey; width: 50px; height: 50px; margin: 10px"></div><span style="align-self: center; margin: 10px">AVAILABLE</span>
          </div>
          
        </div>
      </div>
    </main>

    <footer>
      <div class="container py-4 text-center">
        <p>&copy; 2023 Restoran Triwahyudi. All rights reserved.</p>
      </div>
    </footer>
    <b-modal v-model="popup" title="Booking Meja" centered hide-footer hide-header-close no-close-on-backdrop>
      <!-- Konten dari komponen popup di sini -->
      <template>
        <b-form-group label="Nomor Meja">
            <b-form-input type="text" v-model="numberTablePopup" required readonly></b-form-input>
        </b-form-group>
        <b-form-group label="Nama Reservasi" class="mt-4">
            <b-form-input type="text" v-model="namaReservasi" id="nama-reservasi" required></b-form-input>
        </b-form-group>
        <b-form-group label="Menu (minimal pilih 2)" class="mt-4">
            <b-form-checkbox-group v-model="pilihanMenu" :options="menus" required>

            </b-form-checkbox-group>
        </b-form-group>
        <div class="mt-4 d-flex flex-row justify-content-evenly">
          <b-button v-if="!isOrder" variant="primary" @click="createOrder()">Order</b-button>
          <b-button v-if="!isOrder" @click="closePopup()">Close</b-button>
          <b-button v-if="isOrder" variant="primary" @click="addOrder()">Order Again</b-button>
          <b-button v-if="isOrder" variant="success" @click="closeOrder()">Finish Order</b-button>
        </div>
      </template>
    </b-modal>
  </body>
  
</html>
  
</template>

<script>
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { menuService } from '@/_services/menu-service';
import { mejaService } from '@/_services/meja-service';
import { orderService } from '@/_services/order-service';

export default {
  name: 'HomeView',
  data() {
    return {
      tables: [],
      popup: false,
      numberTablePopup: 0,
      namaReservasi: null,
      pilihanMenu: [],
      menus: [],
      isOrder: false,
      orderId: null,
    }
  },
  methods: {
    chooseTable(number) {
      this.popup = true;
      this.numberTablePopup = number;
      localStorage.setItem('numberTablePopup', number);
      localStorage.setItem('popup', this.popup);
    },
    closePopup() {
      this.popup = false;
      this.numberTablePopup = 0;
      localStorage.setItem('numberTablePopup', 0);
      localStorage.setItem('popup', this.popup);
    },
    createOrder(){
      if(this.namaReservasi && (this.pilihanMenu.length > 1)){
        const data = {
          reservasi: this.namaReservasi,
          selected_menu: this.pilihanMenu,
          tables: this.numberTablePopup,
          status_order: 'Terbuka',
        };
        orderService.createOrder(data).then(response => {
          this.orderId = response.data.order_id;
          this.pilihanMenu = [];
          document.getElementById('nama-reservasi').readOnly = true;
          this.isOrder = true;
          localStorage.setItem('orderOrNot', this.isOrder);
          localStorage.setItem('namaReservasi', this.namaReservasi);
          localStorage.setItem('orderId', this.orderId);
          this.refreshTable();
        });
      }else{
        alert('Fill the form properly');
      }
    },
    refreshTable() {
      mejaService.fetchAllTables()
        .then(response => {
          this.tables = response.data.meja;
        });
    },
    addOrder(){
      if(this.namaReservasi && (this.pilihanMenu.length > 1)){
        const data = {
          reservasi: this.namaReservasi,
          selected_menu: this.pilihanMenu,
          tables: this.numberTablePopup,
          status_order: 'Terbuka',
          order_id: this.orderId
        };
        orderService.createOrder(data).then(() => {
          this.pilihanMenu = [];
        });
      }else{
        alert('Fill the form properly');
      }
    },
    closeOrder(){
      const data = {
        no_meja: this.numberTablePopup,
      };
      orderService.closeOrder(this.orderId, data)
        .then(() => {
          this.orderId = null;
          this.isOrder = false;
          document.getElementById('nama-reservasi').readOnly = false;
          this.namaReservasi = null;
          this.pilihanMenu = [];
          localStorage.setItem('orderOrNot', this.isOrder);
          localStorage.setItem('namaReservasi', this.namaReservasi);
          localStorage.setItem('orderId', this.orderId);
          this.refreshTable();
        });
      
    },
    getTableStatusClass(status) {
      return {
        'table-number': true,
        'table-available': status === 'AVAILABLE',
        'table-occupied': status === 'OCCUPIED',
      };
    },
  },
  mounted(){
    mejaService.fetchAllTables()
        .then(response => {
          this.tables = response.data.meja;
        });
    menuService.fetchAllMenus()
        .then(response => {
          response.data.menus.forEach(menu => {
            this.menus.push({text: menu.nama_menu + ' (Rp. ' + menu.harga + ')', value: menu.id_menu})
          });
        })

    // localStorage.clear();
    const storedNumberTable = localStorage.getItem('numberTablePopup');
    const storedPopup = localStorage.getItem('popup');
    const storedOrderOrNot = localStorage.getItem('orderOrNot');
    const storedNamaReservasi = localStorage.getItem('namaReservasi');
    const storedOrderId = localStorage.getItem('orderId');

    // const storedNumberTable = 0;
    // const storedPopup = false;
    // const storedOrderOrNot = false;
    // const storedNamaReservasi = null;
    // const storedOrderId = null;

    if (storedNumberTable !== null) {
      this.numberTablePopup = parseInt(storedNumberTable);
    }

    if (storedPopup !== null) {
      if (storedPopup === 'false'){
        this.popup = false;
      } else if (storedPopup === 'true') {
        this.popup = true;
      } else if (storedPopup === false) {
        this.popup = false;
      } else if (storedPopup === true) {
        this.popup = true;
      }
    }

    if (storedOrderOrNot !== null) {
      if (storedOrderOrNot === 'false'){
        this.isOrder = false;
      } else if (storedOrderOrNot === 'true') {
        this.isOrder = true;
      } else if (storedOrderOrNot === false) {
        this.isOrder = false;
      } else if (storedOrderOrNot === true) {
        this.isOrder = true;
      }
    }

    if (storedNamaReservasi !== null) {
      if (storedNamaReservasi === 'null') {
        this.namaReservasi = null;
      } else {
        this.namaReservasi = storedNamaReservasi;
      }
      
    } 
    

    if (storedOrderId !== null) {
      this.orderId = storedOrderId;
    }
  },
}

</script>
<style scoped>

.table-number {
  border: 1px solid #ccc;
  padding: 20px;
  margin: 10px;
  text-align: center;
  cursor: pointer;
}
.header-inner {
  background-color: rgba(69, 69, 69, 0.5); 
  padding: 40px;
  color:white;
}
.header {
    background: url('../assets/background.png') center;
    background-size: auto;
    margin-bottom: 20px;
    padding: 0;
}
.info{
  display: flex;
  flex-direction: row;
}
.table-available {
  background-color: lightgray;
}

.table-occupied {
  background-color: red;
  pointer-events: none;
}

body {
  margin: 0;
}
</style>