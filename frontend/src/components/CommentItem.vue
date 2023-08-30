<template>
  <div>
  <article class="media pl-5">
    <!-- User avatar -->
    <figure class="media-left">
      <p class="rounded-img-container-sm">
        <img class="rounded-img" :src="comment.created_by.get_avatar">
      </p>
    </figure>

    <!-- Comment body -->
    <div class="media-content">
      <div class="content">
        <p>
          <strong>
            <RouterLink :to="{name: 'profile', params:{'id': comment.created_by.id}}">{{ comment.created_by.name }}</RouterLink>
          </strong> @{{ comment.created_by.username }} <small class="has-text-grey pl-1">{{ comment.created_at }}</small>
          <br>
          {{ comment.body }}
          <br>
        </p>
      </div>
    </div>

    <!-- Additional actions -->
    <div className="media-right">
      <a id="show-modal" @click="showModal = true">
        <span class="icon"><i class="fas fa-ellipsis-vertical"></i></span>
      </a>
    </div>
  </article>

  <Teleport to="body">
    <!-- Delete comment -->
    <PostActionModal v-if="userStore.user.id === comment.created_by.id" actionType="deleteAction" :show="showModal" @close="showModal = false" @submitted="deleteThisComment">
      <template #icon>
        <i class="fas fa-trash-can fa-stack-1x has-text-white"></i>
      </template>
      <template #header>Delete comment</template>
      <template #body>Are you sure you want to delete this comment? This action cannot be undone.</template>
    </PostActionModal>

    <!-- Report comment -->
    <PostActionModal v-else actionType="reportAction" :show="showModal" @close="showModal = false" @submitted="reportComment">
      <template #icon>
        <i class="fa-regular fa-flag fa-stack-1x has-text-white"></i>
      </template>
      <template #header>Report comment</template>
      <template #body>Thank you for reporting comments that violate our community standards. Please let us know the reason for your report below and we will address the issue promptly.</template>
    </PostActionModal>
  </Teleport>
  </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import PostActionModal from '../components/PostActionModal.vue'

export default {
  setup() {
    const userStore = useUserStore()

    return {
      userStore,
    }
  },
  props: {
    comment: Object
  },
  components: { 
    RouterLink,
    PostActionModal,
  },
  data() {
    return {
      showModal: false,
    }
  },
  methods: {
    // deleteComment() {
    //   axios
    //     .delete(`/api/posts/${this.comment.id}/comment/delete/`)
    //     .then(response => {
    //       console.log('delete ', response.data)
    //       this.showModal = false
    //     })
    //     .catch(error => {
    //       console.error('delete comment error ', error)
    //     })
    // },
    deleteThisComment() {
      console.log('commentitem delete id ', this.comment.id)
      this.$emit('deleted')
      this.showModal = false
    },
    reportComment() {
      axios
        .post(`/api/posts/${this.comment.id}/comment/report/`)
        .then(response => {
          console.log('report ', response.data)
          this.showModal = false
        })
        .catch(error => {
          console.error('report comment error ', error)
        })
    },
  },
}
</script>