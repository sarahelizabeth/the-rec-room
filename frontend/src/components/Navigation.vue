<template>
  <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <div class="navbar-item">
        <RouterLink :to="{ 'name': 'home' }">
          <h1 class="title is-1" id="main-title">WATCH THIS SHIT, YOU GUYS</h1>
        </RouterLink>
      </div>

      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbarBasicExample" class="navbar-menu">
      <div class="navbar-start">
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
          <RouterLink id="navLink" :to="{ 'name': 'chat' }">
            Chat
          </RouterLink>
        </div>

        <div class="navbar-item">
          <RouterLink id="navLink" :to="{ name: 'profile', params: { 'id': userStore.user.id } }">
            Profile
          </RouterLink>
        </div>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <RouterLink :to="{ 'name': 'signup' }" class="button is-primary">
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
</template>

<script>
  // CREATED THIS JUST IN CASE I WANT TO SEPARATE 
  // OUT THE NAV FROM MAIN APP VIEW LATER
  import { useUserStore } from '@/stores/user'

  export default {
    setup() {
      const userStore = useUserStore()
      return {
        userStore
      }
    },
  }
</script>