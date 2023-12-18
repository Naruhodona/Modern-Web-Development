<template>
  <div class="admin-login">
      <b-form-group label="Username">
        <b-form-input type="text" v-model="username" required></b-form-input>
      </b-form-group>
      <b-form-group label="Password">
        <b-form-input type="password" v-model="password" required></b-form-input>
      </b-form-group>
      <b-button @click="login">Login</b-button>
  </div>
</template>

<script>
import { authService } from '@/_services/auth-service';

export default {
  data(){
      return{
        username: null,
        password: null,
        isLoggedIn: false,
        loginError: null,
      }
  },
  methods: {
    async login() {
      try {
        const data = {
          username: this.username,
          password: this.password
        };
        authService.login(data).then(response => {
          this.username = response.data.username;
          this.password = response.data.password
          this.isLoggedIn = true;
          const user = {
            username: this.username,
            password: this.password,
          }
          // Simpan informasi login ke session storage atau local storage
          sessionStorage.setItem('user', JSON.stringify(user));
          if (this.isLoggedIn) {
            this.$router.push({
                name: 'admin',
            })
          }
        });
      } catch (error) {
      // Tangani kesalahan jika login gagal
        this.loginError = 'Login gagal. Periksa kembali email dan password Anda.';
        console.error(error);
      }
    },
  },
  
  mounted (){
      const storedUser = sessionStorage.getItem('user');
      if (storedUser) {
        this.isLoggedIn = true;
      }
      if (this.isLoggedIn) {
        this.$router.push({
            name: 'admin',
        })
      }
  }
}
</script>

<style scoped>

body{
  margin: 0;
}
</style>