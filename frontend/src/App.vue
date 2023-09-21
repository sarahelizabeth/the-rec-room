<template>
  <nav class="navbar is-primary-purple" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <div class="navbar-item">
        <RouterLink :to="{ name: 'home' }">
          <h1 class="title is-1 is-size-3-mobile" id="main-title">
            <!-- The Rec Room -->
            <span class="icon is-large is-medium-mobile has-text-white mr-1">
              <i class="fas fa-icons"></i>
            </span>
            The Rec Room
          </h1>
        </RouterLink>
      </div>

      <a
        @click="showNav = !showNav"
        :class="{ 'is-active': showNav }"
        role="button"
        class="navbar-burger has-text-white"
        aria-label="menu"
        aria-expanded="false"
        data-target="navbar"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div :class="{ 'is-active': showNav }" id="navbar" class="navbar-menu">
      <div v-if="userStore.user.isAuthenticated" class="navbar-start">
        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ name: 'feed' }" @click.native="closeNav"> Feed </RouterLink>
        </div>

        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ name: 'search' }" @click.native="closeNav"> Search </RouterLink>
        </div>

        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ name: 'chat' }" @click.native="closeNav"> Chat </RouterLink>
        </div>

        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ name: 'notifications' }" @click.native="closeNav">
            Notifications ({{ userStore.user.notifications }})
          </RouterLink>
        </div>
      </div>

      <div class="navbar-end">
        <!-- Authenticated user buttons -->
        <div v-if="userStore.user.isAuthenticated" class="navbar-item has-dropdown is-hoverable">
          <figure class="navbar-link">
            <div class="rounded-img-container-xs">
              <img class="rounded-img" :src="userStore.user.avatar" />
            </div>
          </figure>
          <div class="navbar-dropdown is-right">
            <div class="navbar-item">
              <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }" @click.native="closeNav">
                Profile
              </RouterLink>
            </div>
            <hr class="navbar-divider" />
            <a @click="logout" class="navbar-item"> Log out </a>
          </div>
        </div>

        <!-- Unauthenticated user buttons -->
        <div v-else class="navbar-item">
          <div class="buttons">
            <RouterLink
              :to="{ name: 'signup' }"
              class="button is-secondary-purple has-text-white"
              @click.native="closeNav"
            >
              <strong>Sign up</strong>
            </RouterLink>
            <RouterLink :to="{ name: 'login' }" class="button is-light" @click.native="closeNav"> Log in </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <main class="desktop-padding">
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
        userStore,
      }
    },

    data() {
      return {
        showNav: false,
      }
    },

    beforeCreate() {
      this.userStore.initStore()
      const token = this.userStore.user.access

      if (token) {
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
      } else {
        axios.defaults.headers.common['Authorization'] = ''
      }
    },

    methods: {
      logout() {
        this.userStore.removeToken()
        this.$router.push('/login')
      },
      closeNav() {
        this.showNav = false
      },
    },
  }
</script>

<style>
  #main-title {
    font-family: 'Fugaz One', sans-serif;
    color: white;
  }
  #navLink {
    color: white;
    font-size: 1.2rem;
  }

  .navbar-item img {
    max-height: 4rem !important;
  }
  .navbar-dropdown {
    width: 150px;
  }

  @media only screen and (min-width: 768px) {
    .desktop-padding {
      padding: 0.75rem 3rem;
    }
  }

  @media screen and (max-width: 1023px) {
    #navLink {
      color: #50409a;
    }
    .navbar-item:hover {
      background-color: hsl(0, 0%, 96%);
    }
  }
</style>
