<template>
  <div class="columns">
    <!-- Media type feed container -->
    <div class="column is-two-thirds">
      <div class="box p-3">
        <p class="is-size-4 has-text-weight-bold primary-text-purple">{{ title }}s</p>
      </div>

      <!-- All posts -->
      <div v-for="post in posts" :key="post.id" class="block">
        <PostItem :post="post" />
      </div>
    </div>

    <!-- Right side tags and navigation -->
    <div class="column is-one-third">
      <MediaTypes />
      <Trends />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Follows from '../components/Follows.vue'
import Trends from '../components/Trends.vue'
import MediaTypes from '../components/MediaTypes.vue'
import PostItem from '../components/PostItem.vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'MediaTypeView',
  components: {
    Follows,
    Trends,
    MediaTypes,
    PostItem,
  },
  props: {
    media: {
      type: String,
      default: 'test',
    }
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
      title: '',
      body: '',
    }
  },
  mounted() {
    this.getFeed()
  },
  watch: { 
    '$route.params.id': {
      handler: function() {
        this.getFeed()
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    getFeed() {
      const routeId = this.$route.params.id
      if (routeId == '2') {
        this.title = 'Book'
      } else if (routeId == '3') {
        this.title = 'Show'
      } else if (routeId == '4') {
        this.title = 'Film'
      } else if (routeId == '5') {
        this.title = 'Album'
      }

      axios
        .get(`/api/posts/?mediaType=${this.$route.params.id}`)
        .then(response => {
          this.posts = response.data
        })
        .catch(error => {
          console.error('feed error ', error)
        })
    },
  }
}
</script>