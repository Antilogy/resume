<template>
    <p>Group: {{groupId}}</p>
    <div><p>Group size is: {{groupSize}}</p><input v-model.number="groupSize" placeholder="0" type="number" @change="getGroupSize" ></div>
    <div><p>Payment Per Member: {{paymentPerMember.toFixed(2)}} </p></div>
    <p>Items</p>
    <button v-on:click="addItem()">+</button>Add Item<button v-on:click="removeItem()">-</button>
    
    <div v-for="(child, index) in children" :key="child.id">
        <component :is="child" :key="child.id" :id="index" @itemPriceEvent="itemPriceEvent"></component>
    </div>
</template>

<script>
import Item from './item.vue';

/**Base item class to hold different item prices */


export default{

    name: "SplitCheckGroup",
    
    props:{
        groupId: Number,
        paymentPerMember: Number,
        
    },
    data(){
        return{
            children: [],
            count: 0,
            groupSize: 0,
            
            
        }
    },
    methods:{
        /**Add an item */
        addItem: function(){
            
            this.children.push(Item),
            this.count++,
            this.$emit('addItemEvent', this.groupId, this.children.length-1)
            console.log("Append Item")
            
        },
        removeItem: function(){
            this.count--,
            this.$emit('removeItemEvent', this.groupId, this.children.length-1)
            this.children.pop(),
            console.log("Remove Item")
        },
        getChildren: function(){
            return this.children;
        },
        getGroupSize: function(){
            this.$emit('groupSizeEvent', this.groupId, this.groupSize);
        },
        itemPriceEvent: function(itemPrice, id){
            this.$emit('itemPriceEvent', itemPrice, this.groupId, id);
            console.log("itemPriceEvent");
        }
    }
}

</script>