<template>
    <Authenticator>
      <template v-slot="{ user, signOut }">
        <h3>Hello {{ user.username }}!</h3>
        <button @click="signOut">Sign Out</button>
      </template>
    </Authenticator>


    
  
  
    
</template>

<script setup>
import  {Authenticator, useAuthenticator}  from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import { Amplify, Auth } from 'aws-amplify';
import awsconfig from '../aws-exports';
import {defineComponent} from "vue";
import {ref, watch, toRefs} from 'vue'

 /**Default AWS code to create the sign in / sign out components */
// export default {
//   name: 'AuthComp',
//   components:{
//     Authenticator
//   }
// }

// Using AWS Amplify Headless
// https://ui.docs.amplify.aws/vue/connected-components/authenticator/headless
Amplify.configure(awsconfig);
const auth = useAuthenticator();
const {authStatus} = toRefs(auth);//get the reference to the authenticated status
watch(authStatus, (new_val, old_val) =>{
  // console.log(new_val, old_val);
})
// return{
//   user.username,
// }
</script>


