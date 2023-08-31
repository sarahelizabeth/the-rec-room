<template>
  <div class="columns">
    <!-- Welcome text -->
    <div class="column is-5 is-offset-1">
      <div class="box content" style="border: 2px solid #964EC2;">
        <a href="https://www.youtube.com/watch?v=WB8XDk3sQBc" target="_blank" class="primary-text-purple has-text-weight-bold is-size-4">
          Don't Panic! <i class="fas fa-user-astronaut ml-1"></i>
        </a>
        <p class="mt-3">
          If you're reading this, that means Sarah has roped you into testing her <s>stupid</s>
          awesome app! Once you've created an account, you will join the tens of other users of
          <strong class="primary-text-purple has-text-weight-bold">The Rec Room</strong>: a
          movie, TV, music, and book recommendation app for people who don't suck.
        </p>
        <p>
          Once you've given me all of your personal information—including, but not limited to,
          your name, email address, social security number, blood type, and password—you will 
          be able to create trends, chat with other hoopy froods, and—of course—pester your friends 
          and loved ones with recommendations for all your favorite <s>dumb bullshit</s> media.
        </p>
        <p>
          And, of course, <span class="has-text-weight-semibold primary-text-purple">
            don't forget to bring a towel!</span>
        </p>
      </div>
    </div>

    <!-- Sign up form -->
    <div class="column is-5">
      <div class="box" >
        <form v-on:submit.prevent="submitForm">
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

          <div class="field">
            <label class="label">Password</label>
            <p class="control has-icons-left">
              <input v-model="form.password1" class="input" type="password" placeholder="Password">
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
            </p>
          </div>

          <div class="field">
            <p class="control has-icons-left">
              <input v-model="form.password2" class="input" type="password" placeholder="Repeat Password">
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

          <template v-if="messages.length > 0">
            <div class="box has-background-success">
              <p v-for="message in messages" :key="message" class="has-text-white">{{ message }}</p>
            </div>
          </template>

          <div class="field is-grouped is-grouped-centered">
            <div class="control">
              <button class="button is-link">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        email: '',
        username: '',
        name: '',
        password1: '',
        password2: '',
      },
      errors: [],
      messages: [],
    }
  },
  methods: {
    submitForm() {
      this.errors = []
      this.messages = []

      if (this.form.name === '') {
        this.errors.push('Your name is missing')
      }

      if (this.form.email === '') {
        this.errors.push('Your email is missing')
      }

      if (this.form.username === '') {
        this.errors.push('Your username is missing')
      }

      if (this.form.password1 === '') {
        this.errors.push('Your password is missing')
      }

      if (this.form.password1 !== this.form.password2) {
        this.errors.push('Passwords do not match')
      }

      if (this.errors.length === 0) {
        axios
          .post('/api/signup/', this.form)
          .then(response => {
            if (response.data.message === 'success') {
              this.messages.push('User registered successfully! Please activate your account by following the link that was sent to your email.')
              
              this.form.email = ''
              this.form.name = ''
              this.form.username = ''
              this.form.password1 = ''
              this.form.password2 = ''
            } else {
              const data = JSON.parse(response.data.message)
              
              for (const key in data){
                this.errors.push(data[key][0].message)
              }
            }
          })
          .catch(error => {
            console.error('signup error ', error)
          })
      }
    }
  }
}
</script>