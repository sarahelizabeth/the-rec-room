<template>
  <div class="columns">
    <!-- Main section -->
    <div class="column is-two-thirds">
      <!-- Search bar -->
      <div class="box">
        <form method="POST" v-on:submit.prevent="submitForm">
          <div class="field has-addons">
            <p :class="{'is-loading': loading}" class="control has-icons-left is-expanded">
              <input v-model="query" class="input" type="search" placeholder="Search...">
              <span class="icon is-small is-left">
                <i class="fa-solid fa-magnifying-glass"></i>
              </span>
            </p>
            <div class="control">
              <button class="button is-info">Search</button>
            </div>
          </div>
        </form>
      </div>

      <!-- Search results: User -->
      <div class="block">
        <div class="box">
          <div v-if="users.length" class="columns is-multiline">
            <div v-for="user in users" :key="user.id" class="column is-half">
              <article class="media box">
                <!-- Profile image -->
                <figure class="media-left">
                  <div class="rounded-img-container-sm">
                    <img class="rounded-img" :src="user.get_avatar">
                  </div>
                </figure>
                <!-- User name and info -->
                <div class="media-content">
                  <div class="content">
                    <p>
                      <strong>
                        <RouterLink :to="{name: 'profile', params:{'id': user.id}}">{{ user.name }}</RouterLink>
                      </strong>
                      <br>
                      @{{ user.username }}
                    </p>
                  </div>
                </div>
              </article>
            </div>
          </div>
          <div v-else>
            <p class="has-text-grey">No users match your search.</p>
          </div>
        </div>
      </div>

      <!-- Search results: Posts -->
      <div class="block">
        <div class="box">
          <div v-if="posts.length">
            <div v-for="post in posts" :key="post.id">
              <PostItem :post="post" />
            </div>
          </div>
          <div v-else>
            <p class="has-text-grey">No posts match your search.</p>
          </div>
        </div>
      </div>
    </div>
    <!-- Sidebar -->
    <div class="column is-one-third">
      <!-- Figure out how to pass in user as the prop for search view -->
      <!-- <Follows /> -->
      <!-- Replace with "followed by" -->
      <Trends />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Follows from '../components/Follows.vue'
import Trends from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue'

export default {
  name: 'SearchView',
  components: {
    Follows,
    Trends,
    PostItem,
  },
  data () {
    return {
      query: '',
      users: [],
      posts: [],
      loading: false,
    }
  },
  methods: {
    submitForm() {
      this.loading = true
      if (this.query === '' | this.query === ' ') return
      
      axios
        .post('/api/search/', {
          query: this.query
        })
        .then(response => {
          this.users = response.data.users
          this.posts = response.data.posts
          this.loading = false
        })
        .catch(error => {
          console.error('search error ', error)
          this.loading = false
        })
    }
  }
}
</script>