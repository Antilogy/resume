import{createApp} from 'vue'
import App from './qr_code.vue'
import Header from '../../components/Header.vue'
import '../../assets/css/main.css'

createApp(Header).mount('#header');
createApp(App).mount('#qr_code')