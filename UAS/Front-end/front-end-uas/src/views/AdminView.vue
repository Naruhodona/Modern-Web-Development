<template>
    <div class="admin">
        <nav>
            <div>
                <button class="link-button" id="menu" @click="goToMenu">Menu</button>
                <button class="link-button" id="order" @click="goToOrder">Order</button>
                <button class="link-button" id="logout" @click="logOut">Logout</button>
            </div> 
        </nav>
        <router-view />
    </div>
</template>

<script>
import { menuService } from '@/_services/menu-service';
import { orderService } from '@/_services/order-service';

export default {
    data(){
        return{
            menus: [],
            orders: [],
            isLoggedIn: false,
        }
    },
    methods: {
        goToMenu(){
            this.$router.push({
                name: 'menu',
                params: {
                    menus: this.menus,
                }
            });
            document.getElementById('menu').disabled = true;
            document.getElementById('order').disabled = false;
        },
        goToOrder(){
            this.$router.push({
                name: 'order',
                params: {
                    orders: this.orders,
                }
            });
            document.getElementById('menu').disabled = false;
            document.getElementById('order').disabled = true;
        },
        logOut(){
            sessionStorage.removeItem('user');
            this.isLoggedIn = false;
            this.$router.push({
                name: 'admin-login',
            });
        }
    },
    
    mounted (){
        const storedUser = sessionStorage.getItem('user');
        if (storedUser) {
            this.isLoggedIn = true;
            menuService.fetchAllMenus()
                .then(response => {
                    this.menus = response.data.menus;
                });
            orderService.fetchAllOrders()
                .then(response => {
                    this.orders = response.data.orders_with_details
                });
        } else {
            this.$router.push({
                name: 'admin-login',
            })
        }
        
    }
}
</script>

<style scoped>
nav {
    background: url('../assets/background.png') center;
    background-size: auto;
    margin-bottom: 20px;
    padding: 0;
}

nav div {
    display: flex;
    flex-direction: row;
    padding: 40px;
    justify-content: space-evenly;
    background-color: rgba(69, 69, 69, 0.5)
}
.link-button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font: inherit;
    opacity: 1;
    font-size: 24px;
    font-weight: bold;
    padding: 0;
    margin: 0;
}
body{
    margin: 0;
}
</style>