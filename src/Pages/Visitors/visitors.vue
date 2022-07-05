<template>
    <div  class="visitors">
        <Tabs v-bind:data_list="visitor_json" >
            <Tab title='Browser' >Browser</Tab>
            <Tab title='Language' >Language</Tab>
            <Tab title='Country' >Country</Tab>
        </Tabs>
    </div>
    

</template>



<script>
import Tabs from '../../components/Tabs.vue';
import Tab from '../../components/Tab.vue';
const apiEndpoint = 'http://python3-7.eba-cp2mtsp6.us-east-1.elasticbeanstalk.com/api_v1/'
export default{
    name: 'App',
    components:{
        Tab,
        Tabs
    },
    setup(){
        // const visitor_json = ref(null)
        // const onStart = async function(){
            
        //     console.log("Started asyn");
        //     const res =  await fetch(apiEndpoint + 'visitor_info');
        //     const dataJson =  await res.json();
        //     visitor_json.value = dataJson.visitor_data;
        //     console.log(visitor_json);
        //     console.log("Finished asyn");
             
            
        // }
         
        // const visitor_json = null
        // onServerPrefetch( () =>{
        //     // visitor_json.value = await fetch(apiEndpoint + 'visitor_info')
        //     fetch(apiEndpoint + 'visitor_info')
        //     .then(response => response.json())
        //     .then(data=> (visitor_json.value = data.visitor_data));
        // });
        // return{
        //     visitor_json
        // };
        
    },
    
    methods:{
        /**Function used to call the api */
        onStartUp: async function(){
            console.log("Started asyn");
            const gResponse = await fetch(apiEndpoint + 'visitor_info');
            const gObject = await gResponse.json();
            this.visitor_json = gObject.visitor_data;
            console.log("Finished asyn");
        },
        assignTabInfo: function(){

        }
    },
    created(){
        fetch(apiEndpoint + 'visitor_info')
            .then(response => response.json())
            .then(data=> (this.visitor_json["data"] = data));
    },
    data(){
        return{
            visitor_json : {"data":{}}
        }
    }
}
</script>

<style scoped>
.visitors{
    display:flex;
    flex-direction: column;
    width: 50%;
    margin: 0 auto;
}
</style>