<template >
    <input class="item" v-model.number="itemPrice" placeholder="0" type="number" ref='item' @change="getItemPrice">
</template>

<script>
export default{
    name: "Item",
    props:{
        id: Number,
    },
    data(){
        return{
            itemPrice: "",
            
        }
    },
    methods:{
        /**Returns the item Price */
        getItemPrice: function(){
            this.$emit('itemPriceEvent', this.itemPrice, this.id);
            console.log("My item changed")
        }
    }
}

</script>

<style scoped>
.item{
    box-shadow: #73FBD3 0px 0px 0px 3px;
    text-align:right;
    margin-top: 15px;
}
</style>