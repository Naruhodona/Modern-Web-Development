<template>
  <div class="admin-login">
    <div class="login-form">
      <h2>Login admin</h2>
      <b-form-group label="Username">
        <b-form-input type="text" v-model="username" required></b-form-input>
      </b-form-group>
      <b-form-group label="Password">
        <b-form-input type="password" v-model="password" required></b-form-input>
      </b-form-group>
      <b-button @click="login" variant="primary" style="margin-top: 10px;">Login</b-button>
      <div v-if="loginError" class="error-message">
        {{ loginError }}
      </div>
    </div>
      
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
        if(this.username && this.password){
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
          })
        } else {
          alert('Fill the form properly');
        }

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
      } else {
        this.isLoggedIn = false;
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
.admin-login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-form {
  width: 300px;
  padding: 20px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.error-message {
  color: red;
  margin-top: 10px;
}

body{
  margin: 0;
}
</style>