import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  // id: 'user',

  const user = ref({
    isAuthenticated: false,
    id: null,
    name: null,
    username: null,
    email: null,
    avatar: null,
    access: null,
    refresh: null,
  })

  function initStore() {
    console.log('initStore', localStorage.getItem('user.access'))

    if (localStorage.getItem('user.access')) {
      this.user.access = localStorage.getItem('user.access')
      this.user.refresh = localStorage.getItem('user.refresh')
      this.user.id = localStorage.getItem('user.id')
      this.user.name = localStorage.getItem('user.name')
      this.user.username = localStorage.getItem('user.username')
      this.user.email = localStorage.getItem('user.email')
      this.user.avatar = localStorage.getItem('user.avatar')
      this.user.isAuthenticated = true

      this.refreshToken()

      console.log('Initialized user: ', this.user)
    }
  }

  function setToken(data) {
    console.log('setToken', data)

    this.user.access = data.access
    this.user.refresh = data.refresh
    this.user.isAuthenticated = true

    localStorage.setItem('user.access', data.access)
    localStorage.setItem('user.refresh', data.refresh)

    console.log('user.access: ', localStorage.getItem('user.access'))
  }

  function removeToken() {
    console.log('removeToken')

    this.user.refresh = null
    this.user.access = null
    this.user.isAuthenticated = false
    this.user.id = null
    this.user.name = null
    this.user.username = null
    this.user.email = null
    this.user.avatar = null

    localStorage.setItem('user.access', '')
    localStorage.setItem('user.refresh', '')
    localStorage.setItem('user.id', '')
    localStorage.setItem('user.name', '')
    localStorage.setItem('user.username', '')
    localStorage.setItem('user.email', '')
    localStorage.setItem('user.avatar', '')
  }

  function setUserInfo(user) {
    console.log('setUserInfo', user)

    this.user.id = user.id
    this.user.username = user.username
    this.user.name = user.name
    this.user.email = user.email
    this.user.avatar = user.avatar

    localStorage.setItem('user.id', this.user.id)
    localStorage.setItem('user.username', this.user.username)
    localStorage.setItem('user.name', this.user.name)
    localStorage.setItem('user.email', this.user.email)
    localStorage.setItem('user.avatar', this.user.avatar)

    console.log('User', this.user)
  }

  function refreshToken() {
    axios.post('/api/refresh/', {
      refresh: this.user.refresh
    })
    .then((response) => {
      this.user.access = response.data.access

      localStorage.setItem('user.access', response.data.access)

      axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
    })
    .catch(error =>{
      console.log('refresh token ',error)

      this.removeToken()
    })
  }

  return { 
    user, 
    initStore, 
    setToken, 
    removeToken, 
    setUserInfo, 
    refreshToken, 
  }
})