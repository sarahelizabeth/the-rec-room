<template>
  <div class="columns">
    <div class="column is-half is-offset-one-quarter">
      <div class="box">
        <form method="post" @submit.prevent="submitForm">

          <div class="field">
            <label class="label">Email</label>
            <div class="control has-icons-left has-icons-right">
              <input v-model="form.email" @blur="handleBlur($event)" :class="{'is-danger': !isEmailValid}" class="input" type="email" placeholder="A valid email...">
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </div>
            <p v-if="!isEmailValid" class="help is-danger">This email is invalid.</p>
          </div>

          <div class="field">
            <label class="label">Password</label>
            <p class="control has-icons-left has-icons-right">
              <input v-model="form.password" class="input" :type="passwordInputType" placeholder="Password">
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
              <a @click="toggleShowPassword" class="icon is-small is-right is-clickable">
                <i v-if="showPassword" class="fas fa-regular fa-eye"></i>
                <i v-else class="fas fa-regular fa-eye-slash"></i>
              </a>
            </p>
          </div>

          <template v-if="errors.length > 0">
            <div class="box has-background-warning">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <div class="field is-grouped is-grouped-centered mt-4">
            <div class="control">
              <button class="button is-link">
                <span class="icon">
                  <i class="fas fa-right-to-bracket"></i>
                </span>
                <span>Log in</span>
              </button>
            </div>
          </div>
        </Form>
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
        email: '',
        password: '',
      },
      showPassword: false,
      passwordInputType: 'password',
      isEmailValid: true,
      errors: [],
    }
  },
  methods: {
    handleBlur(e) {
      const checkEmail = this.validateEmail(e.target.value)
      if (checkEmail) this.isEmailValid = true
      else this.isEmailValid = false
    },
    toggleShowPassword() {
      if (this.showPassword == false) {
        this.showPassword = true
        this.passwordInputType = 'text'
      } else {
        this.showPassword = false
        this.passwordInputType = 'password'
      }
    },
    async submitForm() {
      const isEmailValid = this.validateEmail(this.form.email)

      if (!isEmailValid) return

      if (this.errors.length === 0) {
      await axios
        .post('/api/login/', this.form)
        .then(response => {
          this.userStore.setToken(response.data)
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access
        })
        .catch(error => {
          console.error('login POST error ', error)
          this.errors.push('The email or password is incorrect, or the user has not been activated.')
        })
      }
      if (this.errors.length === 0) {
      await axios
        .get('/api/me/')
        .then(response => {
            this.userStore.setUserInfo(response.data)
            this.userStore.setUserNotifications()
            this.$router.push('/feed')
        })
        .catch(error => {
            console.error('login GET error', error)
        })
      }
    },
    validateEmail(value) {
      // if (!value || value == '') {
      //   this.errors.push('This field is required.')
      //   return false
      // }

      const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
      if (!regex.test(value)) {
        return false
      }

      return true
    },
  }
}
</script>