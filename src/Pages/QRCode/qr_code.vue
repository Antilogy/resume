<template>
    <div class="qr_code" >

        <div class="qr_block" v-on:click="togglePopup(false)">
            <input v-model="qrdata" placeholder="email@example.com" type="text" v-on:keyup="createQR()">
            <!-- <button @click="createQR()">Create QR Code</button> -->
            
            <canvas id = "qrcode"></canvas>
            <div><p>Input the 6 digit code from your authenticator app</p></div>
            <div><p>If you can't scan a QR Code, input the secret key instead.</p>
                <p>Secret Key: {{qr_secret}}</p></div>
            <input v-model.number="totp_code" placeholder="123 456" type="number" @keyup.enter="verifyUserTOTP()">
        </div>
        
        <button v-on:click="verifyUserTOTP()">Verify TOTP</button>
    </div>
    <div class="popWarning" id="popup">
        <div class="div_header" >
            <p class="div_title" id="drag_header">Status</p>
            <p class="div_close" v-on:click="togglePopup(false)">X</p><!--Close this window-->
        </div>
        <div class="div_message" id="popup_message" >
            <p>{{message}}</p>
        </div>
    </div>

</template>



<script>
import Tabs from '../../components/Tabs.vue';
import Tab from '../../components/Tab.vue';
import QRCode_Vue from '../../components/QRCode_Vue.vue';
import base32Encode from 'base32-encode'
import DragJS from './DragJS';


export default{
    name: 'App',
    
    setup(){
        //setup the draggable element
    //    var dragElement = document.getElementById('drag_header');
    //    var popup_drag = new DragJS(dragElement);

    //    return{
    //     popup_drag
    //    }
        
    },
    
    methods:{
        createQR: function(){
            var QRCode = require('qrcode')
            var qr_app = "QR APP"
            const array = new Uint8Array(20)
            var base32_secret = null
            self.crypto.getRandomValues(array)
            console.log("Original="  + array)
            
            //secret_key must be base32 encoded
            base32_secret = base32Encode(array, 'RFC4648')
            
            
            //qr_code uses keyuri format
            //https://github.com/google/google-authenticator/wiki/Key-Uri-Format
            var qr_data_secret = `otpauth://totp/${encodeURI(qr_app || '')}:${encodeURI(this.qrdata)}?secret=${base32_secret}&digits=6&period=30`
            console.log("uri = " + qr_data_secret)
            var canvas = document.getElementById('qrcode')
            // QRCode.toCanvas(canvas, this.qrdata, function(error){
            //     if(error) console.error(error)
            //     console.log('success!')
            // })
            QRCode.toCanvas(canvas, qr_data_secret).catch(err =>{
                console.error(err)
            })
            this.qr_secret = base32_secret
            this.base32Decode(this.qr_secret)
            
            

        },
        /**Generate HMAC based one-time password 
         * 
         * secret = array of 20 bytes 
         * 
         * counter = the window of valid passcodes 
         * 
         * https://hackernoon.com/how-to-implement-google-authenticator-two-factor-auth-in-javascript-091wy3vh3
        */
        generateHOTP: function(secret, counter){
            const crypto = require('crypto')
            const decoded_secret = this.base32Decode(secret)
            const buffer = Buffer.alloc(8)
            for (let i = 0; i<8;i++){
                buffer[7-i] = counter & 0xff;
                counter = counter >>8;
            }
            const hmac = crypto.createHmac('sha1', Buffer.from(decoded_secret));
            hmac.update(buffer);
            const hmac_result = hmac.digest();
            // steps taken from rfc4226
            // https://datatracker.ietf.org/doc/html/rfc4226?ref=hackernoon.com#page-7
            const offset = hmac_result[hmac_result.length-1] & 0xf ;
            const bin_code = (hmac_result[offset] &0x7f) << 24
                | (hmac_result[offset+1] & 0xff) << 16
                | (hmac_result[offset+2] & 0xff) << 8
                | (hmac_result[offset+3] & 0xff);
            const hotp = bin_code % (10 ** 6); // we will extract the first 6 digits from the code
            return hotp
        }
        ,
        /**Genreating Time-based OTPs */
        generateTOTP: function(secret, window = 0){
            const counter = Math.floor(Date.now() / 30000); //convert time from milliseconds to steps of 30sec.
            return this.generateHOTP(secret, counter + window);
        },
        /**Verify the TOTP code */
        verifyTOTP: function(token, secret, window = 1){
            //don't allow windows that are greater than 2(1min)
            if (Math.abs(+window) > 2){
                console.error('Window size is too large');
                return false;
            }
            // generate the pass codes for the window range
            // Ex. -1 win is 30 seconds in the past, 1 window is 30 sec ahead
            for (let eWindow = -window; eWindow <= +window; eWindow++){
                const totp = this.generateTOTP(secret, eWindow);
                if(token === totp){
                    return true
                }
            }
        },
        /**Verify the user submitted TOTP code */
        verifyUserTOTP: function(){
            if(this.verifyTOTP(this.totp_code, this.qr_secret)){
                // create popup window
                console.log("True");
                this.message = "Success!";
                this.togglePopup(true);
            }
            else{
                console.log("False");
                this.message = "Failure!";
                this.togglePopup(true);
            }
        },

        /**Decode a base32 string and return the byte array*/
        base32Decode: function(password){
            const base32_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
            let new_pass = ""
            let uint8_array = ""
            let byte_group = 0
            let byte_array = null
            for(let x in password){
                new_pass += Number(base32_string.indexOf(password[x])).toString(2).padStart(5, '0')
                
            }
            byte_group = new_pass.length/8
            byte_array = new Uint8Array(byte_group)
            for(let i = 0;i<byte_group;i++){
                // console.log(new_pass.substring(0+i*8,i*8+8))
                // console.log(parseInt(new_pass.substring(0+i*8,i*8+8), 2))
                byte_array[i] = parseInt(new_pass.substring(0+i*8,i*8+8), 2)
            }
            // console.log("Decoded byte array=" + byte_array)
            return byte_array
        },
        /**Toggle the popup warning for TOTP codes. */
        togglePopup: function(display_flag = true){
            var popup = document.getElementById('popup')
            var message = document.getElementById('popup_message')
            if(display_flag){
                
                popup.style.display = 'block';
                popup.style.transform = 'translate(-50%, -50%)';
            }
            else{
                popup.style.display = 'none';
            }
            if(this.message==="Success!"){
                message.style.color = '#00916E'
            }
            else{
                message.style.color = '#D62839'
            }
        },
        
    },
    
    
    created(){
    
    },
    mounted(){
        //setup the draggable element
       var dragElement = document.getElementById('popup');
       var dragHeader = document.getElementById('drag_header');
       var popup_drag = new DragJS(dragElement, dragHeader);

       return{
        popup_drag
       }
    },
    data(){
        return{
           qr_secret: "",
           message: "",
        }
    }
}
</script>

<style scoped>
.qr_code, .qr_block{
    display: flex;
    flex-direction: column;
    /* width: 25%; */
    align-items: center;
    justify-content: center;

}
input[type=text]{
    width: auto;
}
input{
    margin: 10px;
}

/***Popup warning CSS */
.popWarning{
    display: none;
    position: absolute;
    z-index: 999;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    font-weight: bold;
}
.div_header{
    display: flex;
    flex-direction: row;
}
.div_header p{
    margin-bottom: 0px;
}
.div_title{
    width: 200px;
    background: #0BA8E6 ;
    padding-left: 10px
}
.div_close{
    width: 20px;
    background: #D62839;
    color: #ffffff;
    cursor: pointer;
    text-align: center;
    
}
.div_message{
    background: lightgray;
    padding-left:10px;
    
}
/**End of Popup warning css */
</style>