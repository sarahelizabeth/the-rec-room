<template>
  <div class="columns">
    <!-- Chat List Panel -->
    <div class="column is-narrow">
      <article class="panel">
        <p class="panel-heading">Your Chats</p>
        <div v-if="this.chats.length">
          <a
            v-for="chat in chats"
            :key="chat.id"
            @click="setActiveChat(chat.id)"
            class="panel-block pr-5"
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
        </div>
        <div v-else>
          <p class="panel-block pl-4" style="width: 250px">No active threads.</p>
        </div>
      </article>
    </div>

    <!-- Main Chat view -->
    <div class="column has-text-centered">
      <div class="container">
        <img src="/assets/message-icon.png" style="transform: rotate(-10deg)" />
        <!-- <img src="/assets/chat-icon.png" /> -->
        <p class="title">Messages</p>
        <div v-if="this.chats.length">
          <p>Select a name from the panel on the left to view your chats.</p>
        </div>
        <div v-else>
          <p>Start a message with a friend by going to their profile and hitting the "Chat" button!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { useUserStore } from '../stores/user';

  export default {
    name: 'ChatView',
    setup() {
      const userStore = useUserStore();
      return {
        userStore,
      };
    },
    data() {
      return {
        chats: [],
        activeChat: '',
        body: '',
      };
    },
    mounted() {
      this.getChats();
    },
    methods: {
      setActiveChat(id) {
        this.$router.push(`/chat/${id}/`);
      },
      getChats() {
        axios
          .get('/api/chat/')
          .then((response) => {
            this.chats = response.data;
          })
          .catch((error) => {
            console.error('get chat error ', error);
          });
      },
    },
  };
</script>
