import Vue from 'vue'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
import 'element-ui/packages/theme-chalk/lib/index.css'
import {
  Button,
  Container,
  Icon,
  Upload,
  Loading,
  Dialog,
  Image
} from 'element-ui'

const elements = [
  Button,
  Container,
  Icon,
  Upload,
  Loading,
  Dialog,
  Image
]

locale.use(lang)

elements.forEach((El) => Vue.use(El, { locale }))
