<template>
    <div class='qr_code'>
        <p>{{name}}</p>
    <slot></slot>
    </div>
</template>

<script>



export default {
    name: 'QRCode_Vue',
    setup(props, ) {
        
    },
    props:{
        title:{
            type: String,
            default: 'QRCode'

        },
        name:{
            type: String,
            default: 'Generic QRCode'
        }
    },
    data(){
        return{
            isActive: true
        }
    }

}
</script>