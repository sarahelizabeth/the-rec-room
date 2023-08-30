<template>
  <div class="field has-addons">
    <div class="control">
      <button @click="selectType(-1)" :class="selectedId == -1 ? 'is-primary-purple has-text-white is-selected' : ''" class="button">
        <span class="icon is-small">
          <i class="fas fa-layer-group"></i>
          <!-- <i class="fas fa-list"></i> -->
          <!-- <i class="fas fa-house"></i> -->
        </span>
        <span>All</span>
      </button>
    </div>
    <div v-for="item in types" :key="item.id" class="control">
      <button @click="selectType(item.id)" class="button" :class="selectedId == item.id ? mediaClass : ''">
        <span class="icon is-small">
          <i :class="item.icon"></i>
        </span>
        <span>{{ item.name }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MediaTypeButtons',
  data() {
    return {
      types: [],
      selectedId: -1,
      mediaClass: 'is-dark',
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
    },
    selectType(id) {
      this.selectedId = id
      if (id == 3) {
        this.mediaClass = 'is-info is-selected'
      } else if (id == 4) {
        this.mediaClass = 'is-primary is-selected'
      } else if (id == 2) {
        this.mediaClass = 'is-warning is-selected'
      } else if (id == 5) {
        this.mediaClass = 'is-danger is-selected'
      }
      this.$emit('filterMedia', id)
    }
  },
}
</script>