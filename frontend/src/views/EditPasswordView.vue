<template>
  <div class="columns">
    <div class="column is-half is-offset-one-quarter">

      <div class="box">
        <p class="is-size-4 has-text-weight-bold mb-4">Edit Password</p>

        <!-- Start main form -->
        <form v-on:submit.prevent="submitForm">

          <div class="field">
            <label class="label">Old Password</label>
            <p class="control has-icons-left">
              <input v-model="form.old_password" class="input" type="password" placeholder="Old Password">
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
            </p>
          </div>

          <div class="field">
            <label class="label">New Password</label>
            <p class="control has-icons-left">
              <input v-model="form.new_password1" class="input" type="password" placeholder="Password">
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
            </p>
          </div>

          <div class="field">
            <p class="control has-icons-left">
              <input v-model="form.new_password2" class="input" type="password" placeholder="Repeat Password">
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
            </p>
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
        old_password: '',
        new_password1: '',
        new_password2: '',
      },
      errors: [],
    }
  },
  methods: {
    submitForm() {
      this.errors = []

      if (this.form.new_password1 !== this.form.new_password2) {
        this.errors.push('Passwords do not match')
      }

      if (this.form.new_password1 == this.form.old_password) {
        this.errors.push('New password cannot be the same as old password')
      }

      if (this.errors.length === 0) {
        let formData = new FormData()
        formData.append('old_password', this.form.old_password)
        formData.append('new_password1', this.form.new_password1)
        formData.append('new_password2', this.form.new_password2)

        axios
          .post('/api/editpassword/', formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            }
          })
          .then(response => {
            if (response.data.message === 'success') {
              this.$router.push(`/profile/${this.userStore.user.id}`)
            } else {
              const data = JSON.parse(response.data.message)

              for (const key in data){
                this.errors.push(data[key][0].message)
              }
            }
          })
          .catch(error => {
            console.error('edit password error ', error)
          })
      }
    }
  }
}
</script>