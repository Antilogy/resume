import{createApp} from 'vue'
import App from './visitors.vue'
import Header from '../../components/Header.vue'
import '../../assets/css/main.css'

createApp(Header).mount('#header');
createApp(App).mount('#visitors')