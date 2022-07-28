<template>
    <input v-model="qrdata" placeholder="email@example.com" type="text" v-on:keyup="createQR()">
    <button @click="createQR()">Create QR Code</button>
    <QRCode_Vue v-for="(child,index) in children" :key="index" :name="child">
        {{child}}
    </QRCode_Vue>
    <canvas id = "qrcode"></canvas>
    

</template>



<script>
import Tabs from '../../components/Tabs.vue';
import Tab from '../../components/Tab.vue';
import QRCode_Vue from '../../components/QRCode_Vue.vue';
import base32Encode from 'base32-encode'



export default{
    name: 'App',
    
    setup(){
       
       
        
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
         * secret = array of 20 bytes
         * counter = the window of valid passcodes
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
        generateTOTP: function(){

        },
        /**Verify the TOTP code */
        verifyTOTOP: function(){

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
                console.log(new_pass.substring(0+i*8,i*8+8))
                console.log(parseInt(new_pass.substring(0+i*8,i*8+8), 2))
                byte_array[i] = parseInt(new_pass.substring(0+i*8,i*8+8), 2)
            }
            console.log("Decoded byte array=" + byte_array)
            return byte_array
        }
    },
    created(){
        
    },
    data(){
        return{
           qr_secret: ""
        }
    }
}
</script>

<style scoped>

</style>