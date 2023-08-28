<template>
  <div class="columns">
    <div class="column is-half is-offset-one-quarter">

      <div class="box">
        <p class="is-size-4 has-text-weight-bold mb-4">Edit Profile</p>
        <!-- Image container -->
        <div class="container has-text-centered">
          <div class="columns is-centered">
            <div class="column is-full">
              <figure class="rounded-img-container-lg is-inline-block">
                <img class="rounded-img" :src="previewImage" >
              </figure>
            </div>
          </div>
        </div>

        <!-- Start main form -->
        <form v-on:submit.prevent="submitForm">

          <div class="field">
            <label class="label">Avatar</label>
            <div class="file has-name is-fullwidth">
              <label class="file-label">
                <input class="file-input" type="file" ref="file" @change="uploadFile">
                <span class="file-cta">
                  <span class="file-icon">
                    <i class="fas fa-upload"></i>
                  </span>
                  <span class="file-label">
                    Choose File
                  </span>
                </span>
                <span class="file-name is-fullwidth">
                  {{ previewImageURL }}
                </span>
              </label>
            </div>
          </div>

          <div class="field">
            <label class="label">Name</label>
            <div class="control">
              <input v-model="form.name" class="input" type="text" placeholder="Your full name...">
            </div>
          </div>

          <div class="field">
            <label class="label">Username</label>
            <div class="control has-icons-left has-icons-right">
              <!-- Add class binding for "is-success" and/or "is-danger" -->
              <input v-model="form.username" class="input" type="text" placeholder="An awesome username...">
              <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
              </span>
            </div>
            <!-- <p class="help is-success">This username is available</p> -->
          </div>

          <div class="field">
            <label class="label">Email</label>
            <div class="control has-icons-left has-icons-right">
              <!-- Add class binding for "is-success" and/or "is-danger" -->
              <input v-model="form.email" class="input" type="email" placeholder="A valid email...">
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </div>
            <!-- <p class="help is-danger">This email is invalid</p> -->
          </div>

          <div class="container has-text-centered">
            <RouterLink to="/profile/edit/password">
              <button class="button is-text">
                <span class="icon">
                  <i class="fas fa-unlock"></i>
                </span>
                <span>Edit Password</span>
              </button>
            </RouterLink>
          </div>

          <template v-if="errors.length > 0">
            <div class="box has-background-warning">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <div class="field is-grouped is-grouped-centered mt-3">
            <div class="control">
              <RouterLink :to="{ name: 'profile', params: { 'id': userStore.user.id } }">
                <button class="button is-danger is-outlined">
                  <!-- <span class="icon">
                    <i class="fas fa-cancel"></i>
                  </span> -->
                  <span>Cancel</span>
                </button>
              </RouterLink>
            </div>
            <div class="control">
              <button class="button is-link">
                <span class="icon">
                  <i class="fas fa-floppy-disk"></i>
                </span>
                <span>Save Changes</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },
  data() {
    return {
      form: {
        email: this.userStore.user.email,
        username: this.userStore.user.username,
        name: this.userStore.user.name,
      },
      errors: [],
      previewImage: this.userStore.user.avatar || 'https://bulma.io/images/placeholders/128x128.png',
      previewImageURL: 'No file selected',
    }
  },
  methods: {
    uploadFile(e) {
      this.errors = []
      const image = e.target.files[0]
      const reader = new FileReader()

      const supportedFileTypes = ['image/png', 'image/jpg', 'image/jpeg']
      let fileType = e.target.files[0].type

      if (supportedFileTypes.indexOf(fileType) === -1) {
        this.errors.push('Unsupported file type')
        return
      }

      reader.readAsDataURL(image)
      reader.onload = e => {
        this.previewImage = e.target.result
        this.previewImageURL = this.$refs.file.files[0].name
      }
    },
    submitForm() {
      this.errors = []

      if (this.form.name === '') {
        this.errors.push('Your name is missing')
      }

      if (this.form.email === '') {
        this.errors.push('Your email is missing')
      }

      if (this.form.username === '') {
        this.errors.push('Your username is missing')
      }

      if (this.errors.length === 0) {
        let formData = new FormData()
        formData.append('name', this.form.name)
        formData.append('email', this.form.email)
        formData.append('username', this.form.username)
        formData.append('avatar', this.$refs.file.files[0])

        axios
          .post('/api/editprofile/', formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            }
          })
          .then(response => {
            if (response.data.message === 'information updated') {
              this.userStore.setUserInfo({
                  id: this.userStore.user.id,
                  username: this.form.username,
                  name: this.form.name,
                  email: this.form.email,
              })

              this.$router.back()
            } else {
              const data = JSON.parse(response.data.message)
              
              for (const key in data){
                this.errors.push(data[key][0].message)
              }
            }
          })
          .catch(error => {
            console.error('edit profile error ', error)
          })
      }
    }
  }
}
</script>