<template>
    <ul class="main_tabs">
        <li v-for="(child, index) in tab_titles" :key="child" @click="tabFocus(index)">
            {{child}}
            
        </li>
    </ul>
    <div class="tabs_group" >
        <div v-for="(child, index) in children" :key="child" class="tab_item">
            <div class="tab_title">{{child.split(":")[0]}}</div><div class="tab_data" :style="{width:(child_size[index]/100 * 90).toFixed(2).toString() + '%'}"><p>{{child_size[index]}}%</p></div>
        </div>
    </div>
    
</template>

<script>
import {ref} from 'vue'
export default {
    // slots refers to the slot tags in tab
    setup(props,{slots}) {
        const tab_titles = ref(slots.default().map((tab) => tab.props.title))
        
        return{
            tab_titles,
            
        }
    },
    props:{
        data_list:{
            type: Object,
            default(rawProps) {
                return {message:'hello'}
            }
        }
    },
    mounted(){
        
    },
    methods:{
        tabFocus: function(index){
            // first unview the current index
            const dict_keys = Object.keys(this.data_list["data"])
            
            // then show the clicked index
            this.current_index = index;
            this.children = this.data_list['data'][dict_keys[index]]
            
        }
    },
    data(){
        return{
            children: [],
            child_size: [],
            current_index: 0,
            tabs_total: 0
        }
        
    },
    watch:{
        children(value,oldValue){
            this.tabs_total = 0
            let tab_data = document.getElementsByClassName("tab_data")
            for (let child of value){
                this.tabs_total +=parseInt(child.split(":")[1])
            }
            // set the width size of each tab data element
            let index = 0
            this.child_size.length = 0
            for (let child of value){
                this.child_size.push(parseInt(child.split(":")[1])/this.tabs_total * 100)
                index++;
                
            }
            
        }
    }
}
</script>
<style scoped>
.current, .tab_item{
    display: flex;
    align-items: center;
}
.tab_item:hover{
    background:lightslategray
}
.not_selected{
    display: none;
}
ul.main_tabs{
    text-align: center;
    
}
ul.main_tabs li{
    display: inline-block;
    padding: 10px 20px;
    cursor: pointer;
}
ul.main_tabs li:hover{
    background:gray
}


.tab_title{
    width: 10%;
    display: flex;
    justify-content: center;
}

.tab_data{
    background: lightblue;
    margin: 10px;
    height: 20px;
    display: flex;
    align-items: center;
    flex-direction: row-reverse;
}
.tab_data p{
    display: flex;
    flex-direction: row-reverse;
    overflow: visible;
    position: relative;
    left: 60px;
    margin-bottom: 0px;
}
</style>