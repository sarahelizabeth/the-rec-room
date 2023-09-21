<template>
  <div class="columns">
    <!-- Chat List Panel -->
    <div class="column is-narrow">
      <article class="panel">
        <p class="panel-heading">Your Chats</p>
        <a
          v-for="chat in chats"
          :key="chat.id"
          @click="setActiveChat(chat.id)"
          class="panel-block"
          :class="activeChat.id == chat.id ? 'is-active has-background-link-light' : ''"
        >
          <article class="level is-full-width">
            <div class="level-left">
              <div class="level-item">
                <span class="panel-icon">
                  <i class="fas fa-user"></i>
                </span>
                <template v-for="user in chat.users" :key="user.id">
                  <span v-if="user.id !== userStore.user.id" class="has-text-bold"
                    ><strong>{{ user.name }}</strong></span
                  >
                </template>
              </div>
            </div>
            <!-- <div class="level-right">
              <div class="level-item">
                <span><small>{{ chat.modified_at_formatted }} ago</small></span>
              </div>
            </div> -->
          </article>
        </a>
      </article>
    </div>

    <!-- Chat view -->
    <div class="column is-two-thirds">
      <div class="container">
        <h1>Chats</h1>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { useUserStore } from '../stores/user'

  export default {
    name: 'ChatView',
    setup() {
      const userStore = useUserStore()
      return {
        userStore,
      }
    },
    data() {
      return {
        chats: [],
        activeChat: '',
        body: '',
      }
    },
    mounted() {
      this.getChats()
    },
    watch: {
      '$route.params.id': {
        handler: function () {
          this.getMessages()
        },
        deep: true,
        immediate: true,
      },
    },
    methods: {
      setActiveChat(id) {
        this.$router.push(`/chat/${id}/`)
        console.log('main chat view setActiveChat id ', id)
      },
      getChats() {
        axios
          .get('/api/chat/')
          .then((response) => {
            this.chats = response.data
            console.log('main chat view getChats response.data ', response.data)
            if (this.chats.length) {
              this.activeChat = this.chats[0].id
              console.log('main chat view getChats this.chats[0].id ', this.chats[0].id)
              this.getMessages()
            }
          })
          .catch((error) => {
            console.error('get chat error ', error)
          })
      },
      getMessages() {
        axios
          .get(`api/chat/${this.$route.params.id}/`)
          .then((response) => {
            this.activeChat = response.data
            console.log('main chat view getMessages response.data ', response.data)
          })
          .catch((error) => {
            console.error('get chat messages error ', error)
          })
      },
      submitForm() {
        axios
          .post(`api/chat/${this.$route.params.id}/send/`, {
            body: this.body,
          })
          .then((response) => {
            console.log('main chat view submitForm ', response.data)
            this.activeChat.messages.push(response.data)
            this.body = ''
          })
          .catch((error) => {
            console.error('send chat message error ', error)
          })
      },
    },
  }
</script>
