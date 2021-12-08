<template>
    <div id='subtotal'>
      <input v-model.number="subtotal" placeholder="0" type="number">
      <p>Subtotal is: ${{subtotal}}</p>
    </div>
    <div id='total'>
      <input v-model.number="total" placeholder="0" type="number">
      <p>Total is: ${{total}}</p>
    </div>
    <div id='tip'>
      <input v-model.number="tip" placeholder="0" type="number">
      <p>Tip is: {{tip}}%</p>
    </div>
    <div id='group_size'>
      <input v-model.number="group_size" placeholder="0" type="number">
      <p>Group size is: {{group_size}}</p>
    </div>
    <!-- Add button here to separate groups -->

    <div id='per_person'>
      
      <p>Per person: ${{total/group_size}}</p>
    </div>
    <!--Add button to add group -->
    <button v-on:click="addGroup()">Add a Group</button>
    <button v-on:click="deleteGroup()">Delete a Group</button>
    <div v-for="(child) in children" :key="child.groupId">
      <component :is="child" :key="child.name" :groupId="groups"></component>
    </div>
</template>


<script>
import SplitCheckGroup from './group.vue';
export default {
  
  name: 'App',
  methods:{
    /**Add a group */
    addGroup: function(){
      this.children.push(SplitCheckGroup),
      this.groups++,
      console.log("Adding group")
    },
    deleteGroup: function(){
      this.children.pop(),
      this.groups--,
      console.log("Deleting a group")
    },
  },
  
  data(){
    
    return{
      children: [],
      groups: 0,
      subtotal: 0,
      total: 0,
      tip: 0,
      group_size: 0,
      per_person: 0
    }
  }

  
}

</script>