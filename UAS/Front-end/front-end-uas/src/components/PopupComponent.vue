<template>
    <div class="popup">
        <input type="text" v-model="number">
        <button @click="closePopup">Book</button>
    </div>
</template>

<script>
export default {
    props: ['numberTable'],
    data(){
        return{
            number: this.numberTable,
        }
    },
    methods: {
        closePopup(){
            this.$emit('closePopup', {
                number: 0,
            });
        }
    }
}
</script>