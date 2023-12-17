<template>
<html>
  <head>
  <title>Homepage Restoran</title>

  </head>
  <body>
    <header>
      <!-- Header -->
      <div class="container-fluid text-center border border-primary">
        <h1>Selamat Datang di Restoran XYZ</h1>
        <p>Silakan pilih nomor meja Anda:</p>
      </div>
    </header>

    <main>
      <!-- Content -->
      <div class="container">
        <div class="row">
          <!-- Nomor Meja -->
          <div v-for="tableNumber in totalTables" :key="tableNumber" class="col-md-3">
            <div class="table-number" @click="chooseTable(tableNumber)">
              <h3>Table <br> {{ tableNumber }}</h3>
            </div>
            
          </div>
          <button @click="fetchData">Click me</button>
        </div>
      </div>
    </main>

    <footer>
      <!-- Footer -->
      <div class="container py-4 text-center">
        <p>&copy; 2023 Restoran XYZ. All rights reserved.</p>
      </div>
    </footer>
    <b-modal v-model="popupVisible" title="Booking Table" centered hide-footer hide-header-close>
      <!-- Konten dari komponen popup di sini -->
      <template>
        <popup-component v-on:closePopup="closePopup" :numberTable="numberTablePopup" />
      </template>
    </b-modal>
    <!-- <popup-component v-if="popupVisible" v-on:closePopup="closePopup" :numberTable="numberTablePopup" /> -->
  </body>
  
</html>
  
</template>

<script>
import PopupComponent from '../components/PopupComponent.vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { menuService } from '../_services/menu-service.js';

export default {
  name: 'HomeView',
  data() {
    return {
      totalTables: 20,
      popupVisible: false,
      numberTablePopup: 0,
    }
  },
  methods: {
    fetchData() {
      // Lakukan permintaan GET ke URL tertentu
      menuService.fetchAllMenus()
        .then(response => {
          // Handle data yang diterima
          console.log(response.data);
        });
    },
    chooseTable(number) {
      this.popupVisible = true;
      this.numberTablePopup = number;
    },
    closePopup() {
      this.popupVisible = false;
      this.numberTablePopup = 0;
    }
  },
  components: {
    PopupComponent,
  }
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

body {
  margin: 0;
}
</style>