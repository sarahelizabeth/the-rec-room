<template>
  <article class="panel side-panel">
    <p class="panel-heading">
      Trends
    </p>
    <div v-for="trend in trends" :key="trend.id">
    <RouterLink :to="{name: 'trend', params: {id: trend.hashtag}}" class="panel-block is-active">
      <span class="panel-icon">
        <i class="fas fa-hashtag" aria-hidden="true"></i>
      </span>
      <span>{{ trend.hashtag }}</span>
    </RouterLink>
    </div>
  </article>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Trends',
  data() {
    return {
      trends: [],
    }
  },
  mounted() {
    this.getTrends()
  },
  methods: {
    getTrends() {
      axios
        .get('/api/posts/trends/')
        .then(response => {
          this.trends = response.data
        })
        .catch(error => {
          console.error('trends error ', error)
        })
    }
  },
}
</script>