<template>
  <div class="columns">
    <div class="column is-8 is-offset-2">

      <!-- New notifications -->
      <div v-if="notifications.length">
        <p class="is-size-4 has-text-weight-bold has-text-grey pb-4 pt-2">New Notifications</p>
        <article v-for="notification in notifications" :key="notification.id" class="media box">
          <figure class="media-left">
            <RouterLink :to="{name: 'profile', params:{'id': notification.created_by.id}}">
              <div class="rounded-img-container-sm">
                <img class="rounded-img" :src="notification.created_by.get_avatar">
              </div>
            </RouterLink>
          </figure>
          <div class="media-content">
            <div class="content">
              <p>{{ notification.body }}</p>
            </div>
            <div class="level is-mobile">
              <div class="level-left">
                <div class="level-item">
                  <button @click="viewNotification(notification)" class="button is-small is-link">View</button>
                </div>
                <div class="level-item">
                  <button @click="readNotification(notification)" class="button is-small is-light is-link">Mark as Read</button>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <span class="has-text-grey is-size-7">{{ notification.created_at }}</span>
                </div>
              </div>
            </div>
          </div>
        </article>
      </div>
      
      <!-- Read notifications -->
      <p class="is-size-5 has-text-weight-bold has-text-grey-light py-3 mt-4">Viewed Notifications</p>
      <article v-for="notification in readNotifications" :key="notification.id" v-if="readNotifications.length" class="media box has-background-white-ter">
        <figure class="media-left">
          <RouterLink :to="{name: 'profile', params:{'id': notification.created_by.id}}">
            <div class="rounded-img-container-sm">
              <img class="rounded-img" :src="notification.created_by.get_avatar">
            </div>
          </RouterLink>
        </figure>
        <div class="media-content">
          <div class="content">
            <p>{{ notification.body }}</p>
          </div>
          <div class="level is-mobile">
            <div class="level-left">
              <div class="level-item">
                <button @click="viewNotification(notification)" class="button is-small is-outlined">View</button>
              </div>
              <div class="level-item">
                <button @click="readNotification(notification)" class="button is-small is-text">Mark as Unread</button>
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <span class="has-text-grey is-size-7">{{ notification.created_at }}</span>
              </div>
            </div>
          </div>
        </div>
      </article>

      <div v-if="notifications.length === 0 && readNotifications.length === 0" class="block box">
        <p>No notifications.</p>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'notifications',
  data() {
    return {
      notifications: [],
      readNotifications: [],
      watchNotification: 0,
    }
  },
  mounted() {
    this.getNotifications()
  },
  watch: { 
    'watchNotification': {
      handler: function() {
        this.getNotifications()
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    getNotifications() {
      axios
        .get('/api/notifications/')
        .then(response => {
          this.notifications = response.data.newNotifications
          this.readNotifications = response.data.readNotifications
        })
        .catch(error => {
          console.error('notification GET error ', error)
        })
    },
    async viewNotification(notification) {
      axios
        .post(`/api/notifications/read/${notification.id}/`)
        .then(response => {
          if (notification.type_of_notification == 'new_follow') {
            this.$router.push({name: 'profile', params: {id: notification.created_by.id}})
          } else if (notification.type_of_notification == 'new_chat') {
            this.$router.push('/chat')
          } else {
            this.$router.push({name: 'postview', params: {id: notification.post_id}})
          }
        })
        .catch(error => {
          console.error('view notification error ', error)
        })
    },
    readNotification(notification) {
      axios
        .post(`/api/notifications/read/${notification.id}/`, {
          'status': notification.is_read ? 'is_read' : ''
        })
        .then(response => {
          this.notifications.unshift(notification)
          this.watchNotification += 1
        })
        .catch(error => {
          console.error('read notification error ', error)
        })
    }
  },
}
</script>