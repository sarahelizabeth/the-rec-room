<template>
  <article class="panel">
    <p class="panel-heading">
      Follows
    </p>
    <div v-for="follow in follows" :key="follow.id">
      <RouterLink :to="{name: 'profile', params:{'id': follow.id}}" class="panel-block is-active">
        <span class="panel-icon">
          <i class="fas fa-user" aria-hidden="true"></i>
        </span>
        {{ follow.name }}
      </RouterLink>
    </div>
  </article>
</template>

<script>
  import axios from 'axios'
  import { RouterLink } from 'vue-router'
  import { useUserStore } from '@/stores/user'

  export default {
    name: 'Follows',
    setup() {
      const userStore = useUserStore()
      return {
        userStore
      }
    },
    // why isn't this working???
    props: {
      user: Object,
    },
    components: {
      RouterLink
    },
    watch: { 
      '$route.params.id': {
        handler: function() {
          this.getFollows()
        },
        deep: true,
        immediate: true
      }
    },
    data() {
      return {
        follows: []
      }
    },
    mounted() {
      this.getFollows()
    },
    methods: {
      getFollows() {
        axios
          .get(`/api/${this.$route.params.id}/get-follows/`)
          .then(response => {
            this.follows = response.data.profile.follows
          })
          .catch(error => {
            console.error('get follows component error ', error)
          })
      }
    },
  }
</script>