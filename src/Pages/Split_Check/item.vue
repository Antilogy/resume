<template>
    <input v-model.number="itemPrice" placeholder="0" type="number">
</template>

<script>
export default{
    name: "Item",

    data(){
        return{
            itemPrice: 0,
            id: 0
        }
    }
}

</script>