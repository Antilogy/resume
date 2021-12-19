import{createApp} from 'vue'
import App from './split_check.vue'
import Header from '../../components/Header.vue'
import '../../assets/css/main.css'

createApp(Header).mount('#header');
createApp(App).mount('#split_check')