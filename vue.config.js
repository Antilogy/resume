module.exports={
    //options....
    pages:{
        index:{
            entry:'src/main.js',
            template:'public/index.html',
            filename:'index.html',
            title: 'Home',
            chunks:['chunk-vendors', 'chunk-common', 'index']
        },
        vue_index:'src/main.js',
    }
}