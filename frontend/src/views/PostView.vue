<template>
  <div class="columns">
    <div class="column is-two-thirds">

      <!-- Post -->
      <div v-if="post.id" class="block">
        <PostItem :post="post" :user="user" :showDetail="true" />
      </div>

      <!-- Add Additional Recipients -->
      <!-- <div class="card box">
        <div class="field">
          <div class="control">
            <input class="input is-primary" placeholder="Tag recipients here..." />
          </div>
        </div>
      </div> -->

      <!-- Create comment -->
      <div class="block">
        <form method="POST" v-on:submit.prevent="submitForm">
          <div class="field">
            <div class="control">
              <textarea v-model="body" class="textarea" rows="2" placeholder="Word vomit goes here"></textarea>
            </div>
          </div>
          <button class="button is-link">
            <span class="icon">
              <i class="fas fa-paper-plane"></i>
            </span>
            <span>Comment</span>
          </button>
        </form>
      </div>

      <!-- Comment list -->
      <div v-for="comment in post.comments" :key="comment.id" class="block">
        <CommentItem :comment="comment" @deleted="deleteComment(comment.id)" />
      </div>
    </div>

    <!-- Right-hand gutter navigation -->
    <div class="column is-narrow">
      <Trends />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue'
import CommentItem from '../components/CommentItem.vue'

export default {
  name: 'PostView',
  components: {
    Trends,
    PostItem,
    CommentItem
  },
  data() {
    return {
      user: {},
      post: {
        id: null,
        comments: []
      },
      body: ''
    }
  },
  mounted() {
    this.getPost()
  },
  methods: {
    getPost() {
      axios
        .get(`/api/posts/${this.$route.params.id}/`)
        .then(response => {
          this.post = response.data.post
          this.user = response.data.user
        })
        .catch(error => {
          console.error('post detail error', error)
        })
    },
    submitForm() {
      axios
        .post(`/api/posts/${this.$route.params.id}/comment/`, {
          'body': this.body
        })
        .then(response => {
          this.post.comments.push(response.data)
          this.post.comments_count += 1
          this.body = ''
        })
        .catch(error => {
          console.error('comment error', error)
        })
    },
    deleteComment(id) {
      axios
        .delete(`/api/posts/${this.$route.params.id}/comment/${id}/delete/`)
        .then(response => {
          // this.showModal = false
          this.getPost()
        })
        .catch(error => {
          console.error('delete comment error ', error)
        })
    },
  }
}
</script>