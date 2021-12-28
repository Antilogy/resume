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
      <!-- Tip is calculated before tax -->
      <p>Per person: ${{total/group_size + (subtotal/group_size)*(tip/100)}}</p>
    </div>
    <!--Add button to add group -->
    <button v-on:click="addGroup()">Add a Group</button>
    <button v-on:click="deleteGroup()">Delete a Group</button>
    <br>
    <br>
    <button v-on:click ="updateSplitCheck()">Update SplitCheck</button>
    <div class="groups">
      <div v-for="(child, index) in children" :key="child.groupId">
        <!-- Assign the value to a new object to prevent binding -->
        <component :is="child" :key="child.name" :groupId="index" :paymentPerMember="this.groupList[index].paymentPerMember" @groupSizeEvent="groupSizeEvent" @itemPriceEvent="itemPriceEvent" @addItemEvent="addItemEvent" @removeItemEvent="removeItemEvent"></component>
      </div>

    </div>
    
</template>


<script>
import SplitCheckGroup from './group.vue';
import {ref} from 'vue';
import GroupsJS from './GroupsJS';
export default {

  name: 'App',
  methods:{
    /**Add a group */
    addGroup: function(){
      this.paymentPerMember.push(ref(0)),
      this.children.push(SplitCheckGroup),
      this.groupList.push(new GroupsJS(this.groups,ref(0)))
      this.groups++,
      console.log("Adding group"),
      console.log("Group: " + this.groups)
      this.updateSplitCheck()
    },
    deleteGroup: function(){
      this.children.pop(),
      this.groupList.pop(),
      this.groups--,
      console.log("Deleting a group"),
      console.log("Group: " + this.groups)

      this.updateSplitCheck()
    },

    groupSizeEvent: function(groupId, groupSize){
      console.log("GroupID: " + groupId)
      console.log("GroupSize: " + groupSize)
      this.groupList[groupId].groupSize = groupSize


      this.updateSplitCheck()
    },
    
    itemPriceEvent: function(itemPrice, groupId, id){
      this.groupList[groupId].items[id] = itemPrice

      this.updateSplitCheck()
    },
    addItemEvent: function(groupId, itemId){
      this.groupList[groupId].addItem()


      this.updateSplitCheck()
    },
    removeItemEvent: function(groupId, itemId){

      this.groupList[groupId].removeItem()
      this.updateSplitCheck()
    },
    
    /**Updates the total cost per member for each group */
    updateSplitCheck: function(){

      if(this.groupList.length<1){
        return
      }
      

      // Grab total before tax
      var basecost,totalcost,itemcost =0
      var total_people = 0
      var group_costs = []


      // Get total number of people per group
      for (let group in this.groupList){
        var group_item = 0
        total_people += this.groupList[group].groupSize
        // total of all items
        for(let item in this.groupList[group].items){
          
          itemcost += this.groupList[group].items[item]
          group_item += this.groupList[group].items[item]
        }
        group_costs.push(group_item)
      }
      // calculate base cost without items per group
      basecost = (this.subtotal - itemcost)/total_people
      // calculate total cost per person in a group
      for (let i in this.groupList){
        totalcost = (group_costs[i]/this.groupList[i].groupSize) + basecost
        this.groupList[i].paymentPerMember = totalcost * (1 + (this.tip/100) + (this.total-this.subtotal)/this.subtotal)  
      }

    }
  },
  
  data(){
    
    return{
      children: [],
      paymentPerMember: [],
      groupList: [],
      groups: 0,
      subtotal: 0,
      total: 0,
      tip: 0,
      group_size: 0,
      per_person: 0,

    }
  }

  
}

</script>