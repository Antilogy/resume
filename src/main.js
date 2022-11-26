import { createApp } from 'vue'
import App from './App.vue'
import AuthComp from './components/AuthComp.vue'
// import "@aws-amplify/ui-vue/styles.css";
import Auth from "aws-amplify"
import awsConfig from "./aws-exports";

// Auth.configure(awsConfig);
// Amplify.configure(awsConfig);
createApp(App).mount('#app')
// createApp(AuthComp).mount('#authcomp')
