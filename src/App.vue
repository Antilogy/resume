<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import  {Authenticator}  from "@aws-amplify/ui-vue";

import { Amplify, Auth } from 'aws-amplify';
import awsconfig from './aws-exports';
import {defineComponent} from "vue";
// Amplify.configure(awsconfig);
// Auth.configure(awsconfig);
export default {
  name: 'App',
  components: {
    HelloWorld,
    // Authenticator
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
