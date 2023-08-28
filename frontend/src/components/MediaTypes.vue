<template>
  <article class="panel side-panel">
    <p class="panel-heading">
      Media Types
    </p>
    <div v-for="item in types" :key="item.id">
    <RouterLink :to="{name: 'mediatype', params: {id: item.id}, props: {media: item.name}}" class="panel-block is-active">
      <span class="panel-icon">
        <i :class="item.icon" aria-hidden="true"></i>
      </span>
      <span>{{ item.name }}</span>
    </RouterLink>
    </div>
  </article>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MediaTypes',
  data() {
    return {
      types: [],
    }
  },
  mounted() {
    this.getMediaTypes()
  },
  methods: {
    getMediaTypes() {
      axios
        .get('/api/posts/mediatypes/')
        .then(response => {
          this.types = response.data
        })
        .catch(error => {
          console.error('trends error ', error)
        })
    }
  },
}
</script>