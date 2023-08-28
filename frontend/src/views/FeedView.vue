<template>
  <div class="columns">
    <!-- Feed container -->
    <div class="column is-two-thirds">
      <!-- Create post -->
      <div v-if="userStore.user.isAuthenticated">
        <CreatePost :user="null" :posts="posts" />
      </div>

      <!-- All posts -->
      <div v-for="post in posts" :key="post.id" class="block">
        <PostItem :post="post" :showDetail="false" />
      </div>
    </div>

    <!-- Right side tags and navigation -->
    <div class="column is-narrow">
      <MediaTypes />
      <Trends />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CreatePost from '../components/CreatePost.vue'
import Follows from '../components/Follows.vue'
import Trends from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue'
import MediaTypes from '../components/MediaTypes.vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'FeedView',
  components: {
    CreatePost,
    Follows,
    Trends,
    PostItem,
    MediaTypes,
  },
  setup() {
    const userStore = useUserStore()
    return {
      userStore,
    }
  },
  data() {
    return {
      posts: [],
    }
  },
  mounted() {
    this.getFeed()
  },
  methods: {
    getFeed() {
      axios
        .get('/api/posts/')
        .then(response => {
          this.posts = response.data
        })
        .catch(error => {
          console.error('get feed error ', error)
        })
    },
  }
}
</script>
