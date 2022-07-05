module.exports={
    //options....
    pages:{
        index:{
            entry:'src/assets/js/main.js',
            template:'public/index.html',
            filename:'index.html',
            title: 'Home'
            
        },
        split_check:{
            entry:'src/Pages/Split_Check/main.js',
            template:'public/split_check.html',
            filename: 'split_check.html',
            title:'Split Check'
        },
        visitors:{
            entry:'src/Pages/Visitors/main.js',
            template:'public/visitors.html',
            filename: 'visitors.html',
            title:'Visitors'
        },
        vue_index:'src/main.js',
    }
}