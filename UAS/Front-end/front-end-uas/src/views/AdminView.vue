<template>
    <div class="">
        <nav>
            <button @click="goToMenu">Menu</button>
            <button @click="goToOrder">Order</button>
        </nav>
        <router-view />
    </div>
</template>

<script>
import { menuService } from '@/_services/menu-service';

export default {
    data(){
        return{
            menus: [],
            orders: []
        }
    },
    methods: {
        goToMenu(){
            this.$router.push({
                name: 'menu',
                params: {
                    menus: this.menus,
                }
            })
        },
        goToOrder(){
            this.$router.push({
                name: 'order',
                params: {
                    orders: this.orders,
                }
            })
        }
    },
    
    mounted (){
        menuService.fetchAllMenus()
            .then(response => {
                this.menus = response.data.menus;
            });
        // console.log(this.menus);
    }
}
</script>