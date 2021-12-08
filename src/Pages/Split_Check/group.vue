<template>
    <p>Group: {{group-id}}</p>
    <input v-model.number="itemPrice" placeholder="0" type="number"><button v-on:click="addItem()">+</button><button v-on:click="removeItem()">-</button>
    <input v-model.number="groupSize" placeholder="0" type="number">
    <div v-for="(child) in children" :key="child.id">
        <component :is="child" :key="child.id" :id="count"></component>
    </div>
</template>

<script>
import Item from './item.vue';

/**Base item class to hold different item prices */


export default{

    name: "SplitCheckGroup",
    
    props:{
        groupId: Number,
        
        
    },
    data(){
        return{
            children: [],
            count: 0,
            groupSize: 0,
            itemPrice: 0
        }
    },
    methods:{
        /**Add an item */
        addItem: function(){
            this.count++,
            this.children.push(Item),
            console.log("Append Item")
            
        },
        removeItem: function(){
            this.count--,
            this.children.pop(),
            console.log("Remove Item")
        }
    }
}

</script>