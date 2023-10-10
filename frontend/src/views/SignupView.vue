<template>
  <div class="columns">
    <!-- Welcome text -->
    <div class="column is-5 is-offset-1">
      <div class="box content" style="border: 2px solid #964ec2">
        <a
          href="https://www.youtube.com/watch?v=WB8XDk3sQBc"
          target="_blank"
          class="primary-text-purple has-text-weight-bold is-size-4"
        >
          Create Your Profile
        </a>
        <p class="mt-3">
          Once you enter your name and email, come up with a totally rad username, and pick a secure password (at least
          one uppercase letter, one lowercase letter, and one number), you will receive an email containing an
          activation link.
          <strong class="primary-text-purple has-text-weight-bold"
            >You will not be able to log in until you click this link!!</strong
          >
          Once you've done so, come back here and log in to get started with the greatest social media app ever
          conceived by man.
        </p>
      </div>
    </div>

    <!-- Sign up form -->
    <div class="column is-5">
      <div class="box">
        <form v-on:submit.prevent="submitForm">
          <div class="field">
            <label class="label">Name</label>
            <div class="control">
              <input v-model="form.name" class="input" type="text" placeholder="Your full name..." />
            </div>
          </div>

          <div class="field">
            <label class="label">Username</label>
            <div class="control has-icons-left has-icons-right">
              <!-- Add class binding for "is-success" and/or "is-danger" -->
              <input v-model="form.username" class="input" type="text" placeholder="An awesome username..." />
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
              <input v-model="form.email" class="input" type="email" placeholder="A valid email..." />
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </div>
            <!-- <p class="help is-danger">This email is invalid</p> -->
          </div>

          <div class="field">
            <label class="label">Password</label>
            <p class="control has-icons-left has-icons-right">
              <input v-model="form.password1" class="input" :type="passwordInputType" placeholder="Password" />
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
              <a @click="toggleShowPassword" class="icon is-small is-right is-clickable">
                <i v-if="showPassword" class="fas fa-regular fa-eye"></i>
                <i v-else class="fas fa-regular fa-eye-slash"></i>
              </a>
            </p>
          </div>

          <div class="field">
            <p class="control has-icons-left has-icons-right">
              <input v-model="form.password2" class="input" :type="passwordInputType" placeholder="Repeat Password" />
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

          <template v-if="messages.length > 0">
            <div class="box has-background-success">
              <p v-for="message in messages" :key="message" class="has-text-white">{{ message }}</p>
            </div>
          </template>

          <div class="field is-grouped is-grouped-centered">
            <div class="control">
              <button class="button is-link" :class="{ 'is-loading': showLoading }">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

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
        showPassword: false,
        passwordInputType: 'password',
        errors: [],
        messages: [],
        showLoading: false,
      };
    },
    methods: {
      toggleShowPassword() {
        if (this.showPassword == false) {
          this.showPassword = true;
          this.passwordInputType = 'text';
        } else {
          this.showPassword = false;
          this.passwordInputType = 'password';
        }
      },
      submitForm() {
        this.errors = [];
        this.messages = [];

        if (this.form.name === '') {
          this.errors.push('Your name is missing');
        }

        if (this.form.email === '') {
          this.errors.push('Your email is missing');
        }

        if (this.form.username === '') {
          this.errors.push('Your username is missing');
        }

        if (this.form.password1 === '') {
          this.errors.push('Your password is missing');
        }

        if (this.form.password1 !== this.form.password2) {
          this.errors.push('Passwords do not match');
        }

        if (this.errors.length === 0) {
          this.showLoading = true;

          axios
            .post('/api/signup/', this.form)
            .then((response) => {
              this.showLoading = false;
              if (response.data.message === 'success') {
                // could get rid of submit button altogether
                this.messages.push(
                  'User registered successfully! Please activate your account by following the link that was sent to your email.'
                );

                this.form.email = '';
                this.form.name = '';
                this.form.username = '';
                this.form.password1 = '';
                this.form.password2 = '';
              } else {
                const data = JSON.parse(response.data.message);

                for (const key in data) {
                  this.errors.push(data[key][0].message);
                }
              }
            })
            .catch((error) => {
              console.error('signup error ', error);
              this.showLoading = false;
            });
        }
      },
    },
  };
</script>
