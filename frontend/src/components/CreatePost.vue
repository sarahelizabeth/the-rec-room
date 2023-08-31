<template>
  <div class="card box">
    <div @click="handleShowForm" class="px-4 ml-2">
      <a class="is-size-4 has-text-weight-bold">
        <span>Create Recommendation</span>
        <span :style="{transform: `rotate(${deg}deg)`}" class="rotation icon is-large">
          <i class="fas fa-plus"></i>
        </span>
      </a>
    </div>

    <!-- Create post form -->
    <form :class="showForm ? 'showing' : 'hidden'" method="POST" @submit.prevent="submitForm">
      <div class="card-content pt-2">
        
        <!-- Media type field -->
        <div class="field">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="media_type" @change="getGenres($event)">
                <option value="" disabled selected>Choose a media type...</option>
                <option v-for="option in mediaTypes" :key="option.id" :value="option.id" class="has-text-grey">{{ option.name }}</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Title field -->
        <div class="field">
          <div class="control">
            <input v-model="title" class="input" type="text" placeholder="Recommendation title...">
          </div>
        </div>

        <!-- Body field -->
        <div class="field">
          <div class="control">
            <textarea v-model="body" class="textarea" rows="2" placeholder="A short description..."></textarea>
          </div>
        </div>

        <!-- Genre/s field -->
        <div class="field">
          <div class="control">
            <VueMultiselect 
              label="name"
              placeholder="Choose genres..." 
              track-by="id" 
              v-model="genres"
              :max="maxGenres"
              :options="genreOptions" 
              :clear-on-select="true" 
              :close-on-select="true"
              :disabled="genreDisabled"
              :loading="genresLoading"
              :multiple="true"
              :preselect-first="false"
              :preserve-search="false" 
              :tagging="true" />
          </div>
        </div>

        <!-- Recipients field -->
        <div class="field">
          <div class="control">
            <VueMultiselect 
              label="name"
              placeholder="Choose recipients..."
              track-by="id"
              v-model="recipients"
              :options="users"
              :clear-on-select="true" 
              :close-on-select="true"
              :loading="usersLoading"
              :multiple="true"
              :preselect-first="false"
              :preserve-search="false" 
              :tagging="true" />
          </div>
        </div>
      </div>

      <div class="card-footer px-4">
        
        <!-- Add link -->
        <div class="card-footer-item">
          <div v-if="showLinkInput" class="field" style="width: 100%;">
            <div class="control is-expanded">
              <input v-model="link" @blur="handleBlur" :class="{'is-danger': !isLinkValid}" class="input is-fullwidth" type="text" placeholder="http://www.youtube.com">
            </div>
            <p v-if="!isLinkValid" class="help is-danger">This link is invalid</p>
          </div>
          <button v-else @click="showLinkInput = true" class="button is-link">
            <span class="icon">
              <i class="fas fa-paperclip"></i>
            </span>
            <span>Add Link</span>
          </button>
        </div>

        <!-- Post button -->
        <div class="card-footer-item">
          <button class="button is-secondary-purple has-text-white">
            <span class="icon">
              <i class="fas fa-paper-plane"></i>
            </span>
            <span>Post</span>
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import VueMultiselect from 'vue-multiselect'

export  default {
  components: {
    VueMultiselect
  },
  props: {
    user: Object,
    posts: Array
  },
  data() {
    return {
      showForm: false,
      media_type: '',
      title: '',
      body: '',
      recipients: '',
      genres: '',
      link: '',
      showLinkInput: false,
      isLinkValid: true,
      mediaTypes: [],
      genreDisabled: true,
      genreOptions: [],
      maxGenres: 7,
      genresLoading: false,
      users: [],
      usersLoading: true,
      deg: 0,
    }
  },
  mounted() {
    this.getUsers()
    this.getMediaTypes()
  },
  computed: {
    validLink() {
      const pattern = /(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?/g
      const testLink = pattern.test(this.link)

      return testLink
    }
  },
  methods: {
    getUsers() {
      axios
        .get('/api/get-users/')
        .then(response => {
          this.users = response.data
          this.usersLoading = false
        })
        .catch(error => {
          console.error('get users error ', error)
        })
    },
    getMediaTypes() {
      axios
        .get('/api/posts/mediatypes/')
        .then(response => {
          this.mediaTypes = response.data
        })
        .catch(error => {
          console.error('trends error ', error)
        })
    },
    getGenres(event) {
      this.genresLoading = true
      axios
        .get(`/api/posts/genres/?mediaType=${event.target.value}`)
        .then(response => {
          this.genreOptions = response.data
          this.genresLoading = false
          this.genreDisabled = false
        })
        .catch(error => {
          this.genresLoading = false
          console.error('get genres error ', error)
        })
    },
    handleShowForm() {
      this.deg += 45
      this.showForm = !this.showForm
    },
    handleBlur() {
      if (this.validLink) this.isLinkValid = true
      else this.isLinkValid = false
    },
    submitForm() {
      let recipientIds = []
      let genreIds = []
      if (this.recipients.length > 0) {
        recipientIds = this.recipients.map(e => e.id)
      }
      if (this.genres.length > 0) {
        genreIds = this.genres.map(e => e.id)
      }

      if (this.showLinkInput) {
        if (this.validLink) this.isLinkValid = true
        else {
          this.isLinkValid = false
          return
        }
      }

      axios
        .post('/api/posts/create/', {
          'body': this.body,
          'title': this.title,
          'link': this.link,
          'media_type': this.media_type,
          'recipients': recipientIds,
          'genres': genreIds,
        })
        .then(response => {
          this.posts.unshift(response.data)
          this.body = ''
          this.title = ''
          this.link = ''
          this.media_type = ''
          this.recipients = ''
          this.genres = ''
          
          this.genreDisabled = true
          this.showForm = false
        })
        .catch(error => {
          console.error('post form error ', error)
        })
    }
  },
}
</script>

<style>
.rotation {
  transition: transform 0.3s ease-out;
}

.hidden {
  transition: height 0.5s ease 0.3s, opacity 0.3s ease-in;
  height: 0px;
  opacity: 0;
}
.showing {
  transition: height 0.5s ease, opacity 0.3s ease-in 0.35s;
  height: 370px;
  opacity: 1;
}
</style>