<template>
<ul>
    <li>
        <ul class="main_list">
            <li><a href="/">Home</a></li>
            <li><a>WebApps &#9662;</a>
                <ul class="dropdown">
                    <li><a href="/split_check">Split Check</a></li>
                    <li><a href="/visitors">Visitor Info</a></li> 
                    <li><a href="/qr_code">QR Code</a></li>  
                </ul>
            </li>
            <li><a href="https://github.com/Antilogy?tab=repositories">Github Projects</a></li>
        </ul>
    </li>
    <li class="sign_in" >
        <a @click = "(e)=>toggleSignIn(e)">{{sign_in_prompt}} &#9662;</a>
        <div id="auth">
         <AuthComp>
            
        </AuthComp>   
        </div>
        
        
        
        
    </li>
    
</ul>

</template>


<script>

import {createApp, toRefs} from 'vue'
import {Amplify} from 'aws-amplify';
import awsconfig from'../aws-exports'
import AuthComp from './AuthComp.vue';
import  {Authenticator, useAuthenticator}  from "@aws-amplify/ui-vue";
import { isTerminatorless } from '@babel/types';
export default {
    name: "Header",
    components: { AuthComp },
    setup(props, {slots}){
        const auth = useAuthenticator();
        const {authStatus} = toRefs(auth);//Used to keep track of authenticated status
        const sign_in_messages = ["Sign In", "Sign Out"]

        return{
            sign_in_messages,
            authStatus
        }
    },
    data(){
        
        return{
            sign_in_prompt: "Sign In" ,
        }
    },
    
    methods:{
        toggleSignIn: function(event){
            let item = document.getElementById("auth");
            // only allow clicks on the parent 
            if(event.target === event.currentTarget){
                
                if(item.style.display === "none"){
                    item.style.display = "flex"
                }
                else if(item.style.display === ""){
                    // initialize by setting display to flex
                    item.style.display = "flex"
                }
                else{
                    item.style.display = "none"
                }
            }
            else{
                return;
                
            }
            
            
        }
    },
    watch:{
        authStatus(new_val, old_val){
            if(new_val === "authenticated"){
                this.sign_in_prompt = this.sign_in_messages[1] //Sign Out

            }
            else{
                this.sign_in_prompt = this.sign_in_messages[0] //SIgn In
            }
        }
    }
}


</script>


<style scoped>
    ul li.sign_in:last-child{
        float: right
    }

    ul li ul{
        margin: 0;
    }
    ul{
        padding: 0;
        list-style: none;
        background: #333333;
    }
    ul li{
        display: inline-block;
        position: relative;
        line-height: 21px;
        text-align: left;
    }
    ul li a{
        display: block;
        padding: 8px 25px;
        color: #ffffff;
        text-decoration: none;
        cursor: pointer;
    }
    ul li a:hover{
        color: #ffffff;
        background: #111111;
    }
    ul li ul.dropdown{
        min-width: 100%; /* Set width of the dropdown */
        background: #333333;
        display: none;
        position: absolute;
        z-index: 999;
        left: 0;
    }
    ul.main_list li:hover ul.dropdown{
        display: block;	/* Display the dropdown */
        
    }
    ul li ul.dropdown li{
        display: block;
    }
    li.sign_in a{
        pointer-events: auto;
        cursor: pointer;
    }
    .sign_in{
        -webkit-user-select: none;
        user-select: none;
        
    }
    #auth{
        position: absolute;
        z-index: 999;
        display:none;
        flex-direction:column;
        right:0px;
        -webkit-user-select: none;
        user-select: none;
    }


</style>
