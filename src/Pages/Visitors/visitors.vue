<template>
    <div  class="visitors">
        <div id='instructions'>
          <p>Welcome to the Visitors app. 
            <br>
            Directions: Click on a tab to show browser information from visitors that land on the homepage.
            <br>
            No tabs are selected by default.
            <br>
            How it works: 
            <br>
            Step 1.The python backend sends the  IP address from the request to ipinfo.io 
            <br>
            Step 2. Then the following attributes are saved in a mysql table:
            <br>
            <ul>
                <div v-for="(item,index) in ipinfo_list" :key="index">
                <li><p>{{item}}</p></li>
                </div>
            </ul>
            
            
          
          </p>
        </div>
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


var apiEndpoint = 'https://spielbm.com/api_v1/'
let hostname = window.location.host;
try{
    const path = require ("path");

    
    apiEndpoint = 'https://' + hostname + '/api_v1/';
    
} catch (error){
    console.log("Running in production.")
}



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
        const ipinfo_list = ['IP Address', 'Browser Family', 'Browser Version',
         'Language', 'Country', 'Region', 'City', 'Postal code', 'Timezone']
        return{
            ipinfo_list
        }
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
            .then(data=> (this.visitor_json["data"] = data))
            .catch(error=>{
                console.log("Couldn't fetch data. Please make sure you are using HTTPS, your corporate network isn't blocking connections, and try again.");
                alert("Couldn't fetch data. Please make sure you are using HTTPS, your corporate network isn't blocking connections, and try again.")
            });
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
a{
    text-decoration: none;
}
li p{
    margin-bottom:0px;
}
</style>