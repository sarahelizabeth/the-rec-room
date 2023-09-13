<template>
  <nav class="navbar is-primary-purple" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <div class="navbar-item">
        <RouterLink :to="{ 'name': 'home' }">
          <h1 class="title is-1 ml-5" id="main-title">
            <!-- The Rec Room -->
            <span class="icon is-large has-text-white mr-1">
              <i class="fas fa-icons"></i>
            </span>
            The Rec Room
          </h1>
        </RouterLink>
      </div>

      <a @click="showNav = !showNav" :class="{'is-active': showNav}" role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div :class="{'is-active': showNav}" id="navbarBasicExample" class="navbar-menu">
      <div v-if="userStore.user.isAuthenticated" class="navbar-start">
        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ 'name': 'feed' }">
            Feed
          </RouterLink>
        </div>

        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ 'name': 'search' }">
            Search
          </RouterLink>
        </div>

        <div class="navbar-item">
          <!-- <RouterLink id="navLink" :to="{ 'name': 'chat' }">
            Chat
          </RouterLink> -->
        </div>

        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ 'name': 'notifications' }">
            Notifications ({{ userStore.user.notifications }})
          </RouterLink>
        </div>
      </div>

      <div class="navbar-end">

        <!-- Authenticated user buttons -->
        <div v-if="userStore.user.isAuthenticated" class="navbar-item has-dropdown is-hoverable">
          <figure class="navbar-link">
            <div class="rounded-img-container-xs">
              <img class="rounded-img" :src="userStore.user.avatar">
            </div>
          </figure>
          <div class="navbar-dropdown is-right">
            <div class="navbar-item">
              <RouterLink :to="{ name: 'profile', params: { 'id': userStore.user.id } }">
                Profile
              </RouterLink>
            </div>
            <hr class="navbar-divider">
            <a @click="logout" class="navbar-item">
              Log out
            </a>
          </div>
        </div>

        <!-- Unauthenticated user buttons -->
        <div v-else class="navbar-item">
          <div class="buttons">
            <RouterLink :to="{ 'name': 'signup' }" class="button is-secondary-purple has-text-white">
              <strong>Sign up</strong>
            </RouterLink>
            <RouterLink :to="{ 'name': 'login' }" class="button is-light">
              Log in
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <main class="px-6 py-3">
    <RouterView />
  </main>

</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },

  data() {
    return {
      showNav: false
    }
  },

  beforeCreate() {
    this.userStore.initStore()
    const token = this.userStore.user.access

    if (token) {
      axios.defaults.headers.common["Authorization"] = 'Bearer ' + token
    } else {
      axios.defaults.headers.common["Authorization"] = ''
    }
  },

  methods: {
    logout() {
      this.userStore.removeToken()
      this.$router.push('/login')
    }
  }
}
</script>

<style>
  #main-title { font-family: 'Fugaz One', sans-serif; color: white; }
  #navLink { color: white; font-size: 1.2rem; }

  .navbar-item img {
    max-height: 4rem !important;
  }
  .navbar-dropdown {
    width: 150px;
  }
</style>