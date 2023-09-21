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
        <template v-for="message in activeChat.messages" :key="message.id">
          <!-- Outgoing message -->
          <div v-if="message.created_by.id == userStore.user.id" class="columns">
            <div class="column is-full">
              <div class="chat-right box">
                <article class="media">
                  <div class="media-content">
                    <div class="content">
                      <p>
                        <!-- <strong>Me</strong> <small>22m</small>
                        <br> -->
                        {{ message.body }}
                        <br />
                        <span class="block"
                          ><small>{{ message.created_at }}</small></span
                        >
                      </p>
                    </div>
                  </div>
                  <div class="media-right">
                    <figure class="rounded-img-container-sm">
                      <img class="rounded-img" :src="message.created_by.get_avatar" alt="Image" />
                    </figure>
                  </div>
                </article>
              </div>
            </div>
          </div>

          <!-- Incoming message -->
          <div v-else class="columns">
            <div class="column is-full">
              <div class="chat-left box has-background-info">
                <article class="media">
                  <div class="media-left">
                    <figure class="rounded-img-container-sm">
                      <img class="rounded-img" :src="message.created_by.get_avatar" alt="Image" />
                    </figure>
                  </div>
                  <div class="media-content">
                    <div class="content">
                      <p class="has-text-white">
                        <!-- <strong class="has-text-white">Sauron the Deceiver</strong> <small>@eyeofsauron</small> <small>31m</small>
                        <br> -->
                        {{ message.body }}
                        <br />
                        <span class="block"
                          ><small>{{ message.created_at }}</small></span
                        >
                      </p>
                    </div>
                  </div>
                </article>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- Message text box -->
      <div class="container">
        <div class="columns">
          <div class="column">
            <div v-if="chats.length > 0" class="chat-textarea box">
              <article class="media">
                <div class="media-content">
                  <form v-on:submit.prevent="submitForm">
                    <div class="field">
                      <p class="control">
                        <textarea v-model="body" class="textarea" rows="2" placeholder="Pop off, yo..."></textarea>
                      </p>
                    </div>
                    <nav class="level">
                      <div class="level-right">
                        <div class="level-item">
                          <button class="button is-primary">
                            <span class="icon">
                              <i class="fa-regular fa-paper-plane"></i>
                            </span>
                            <span>Send</span>
                          </button>
                        </div>
                      </div>
                    </nav>
                  </form>
                </div>
              </article>
            </div>
            <!-- No chats message -->
            <div v-else class="box">
              <p>Start a chat with another user by going to their profile clicking the "Chat" button!</p>
            </div>
          </div>
        </div>
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
        console.log('chat detail setActiveChat id ', id)
      },
      getChats() {
        axios
          .get('/api/chat/')
          .then((response) => {
            this.chats = response.data
            console.log('chat detail getChats response.data ', response.data)
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
            console.log('chat detail getMessages response.data ', response.data)
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
            console.log('chat detail submitForm ', response.data)
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
