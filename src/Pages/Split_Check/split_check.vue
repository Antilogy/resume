<template>
  <div class="split_check">
    <div id='split_intro'>
        <div id='instructions'>
          <p>Welcome to the SplitCheck app. 
            <br>
            Step 1. Fill in the fields on the left based on the receipt at the end of a restaurant visit. Tips are usually 15% or 18% of the final order.
            <br>
            Step 2. Select Before or After if the receipt shows the tip is applied before the total or after.
            <br>
            Step 3. If you need to split special items like beer because not everyone drinks, then create two groups. The first group has the people that didn't drink while the second group has the cost of the item and the number of people that shared that cost.
          
          </p>
        </div>

      <div id='calc_group'>
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
          <br>
          <p>{{before_after}} Total Tip Amount${{(tip_amount).toFixed(2)}}</p>
          <div id='before_after_tip'>
            <input type="radio" id="before_radio" value="Before" v-model="before_after" v-on:change="updateTipUsed()">
            <label for="before_radio">Before</label>

            <input type="radio" id="after_radio" value="After" v-model="before_after" v-on:change="updateTipUsed()">
            <label for="after_radio">After</label>
              
          </div>
        </div>
        <div id='group_size'>
          <input v-model.number="group_size" placeholder="0" type="number">
          <p>Group size is: {{group_size}}</p>
        </div>
        
        <!-- Add button here to separate groups -->

        <div id='per_person'>
          <!-- Tip is calculated before tax -->
          <p>Per person: ${{((total + tip_amount)/group_size).toFixed(2)}}</p>
        </div>
        <div id='full_cost'>
          <!-- need to implicitly convert total to a number since it defaults to empty string -->
          <p>Full Cost: ${{(total*1 + tip_amount).toFixed(3)}}</p>
          </div>
      </div>

      

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
    /**Update tip used based on whether its applied to subtotal or total */
    updateTipUsed: function(){
      if(this.before_after === "Before"){
        this.tip_amount = this.subtotal*(this.tip/100)
      } else{
        this.tip_amount = this.total*(this.tip/100)
      }
      
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
        if (this.before_after === "Before"){
          this.groupList[i].paymentPerMember = totalcost * (1 + (this.tip/100) + (this.total-this.subtotal)/this.subtotal)
        } else{
          // (totalcost + tax) *(1+tip) 
          this.groupList[i].paymentPerMember = totalcost * (1 + (this.total-this.subtotal)/this.subtotal) * (1+(this.tip/100) )
        }
          
      }

    }
  },
  
  data(){
    
    return{
      children: [],
      paymentPerMember: [],
      groupList: [],
      groups: 0,
      subtotal: "",
      total: "",
      tip: "",
      tip_amount: 0,
      before_after: "After",
      group_size: "",
      per_person: 0,

    }
  }

  
}

</script>

<style scoped>
/* Color theme from https://coolors.co/73fbd3-44e5e7-59d2fe-4a8fe7-5c7aff */
.split_check{
  margin: auto;
  width: 79%;
  border: 3px solid green;
  padding: 10px;
}
input,select{
  text-align: right;
}
select{
  width: 13%;
}
.groups{
  display:flex;
  flex-wrap: wrap;
  overflow-x: auto;
}

@media only screen and (max-width: 500px){
  .split_check{
    width: 79%;
  }
  select{
    width:43%
  }
}

</style>