<template>
  <article class="media box">

    <!-- Profile image -->
    <figure class="media-left">
      <div class="rounded-img-container-sm">
        <img class="rounded-img" :src="post.created_by.get_avatar">
      </div>
    </figure>

    <!-- Main recommendation -->
    <div class="media-content">
      <div class="content">
        <span>
          <strong>
            <RouterLink :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</RouterLink>
          </strong>
          recommended 
          <strong>{{ post.title }}</strong>
          <span v-if="post.recipients?.length > 0">
            to <strong>{{ post.recipients.map(e => e.name).join(', ')}}</strong>
          </span>
        </span>
        
        <div class="py-1">
          <span :class="mediaClass" class="tag mr-2">{{ post.media_type.name }}</span>
          <span v-for="genre in post.genres" :class="mediaClass" class="tag is-light mr-2">{{ genre.name }}</span>
        </div>
        <span v-if="showDetail">{{ post.body }}</span>
        <!-- Link card -->
        <LinkCard v-if="showDetail && post.link" :link="post.link" class="my-4" />
      </div>

      <!-- Bottom elements -->
      <nav class="level is-mobile">
        <div class="level-left">
          <div class="level-item" @click="likePost(post.id)">
            <a :class="{'has-text-danger': isLiked, 'has-text-grey': !isLiked}" class="icon is-small"><i class="fas fa-heart"></i></a>
            <span class="pl-2">{{ post.likes_count }} likes</span>
          </div>
          <div class="level-item">
            <RouterLink :to="{name: 'postview', params: {'id': post.id}}">
              <span class="icon is-small"><i class="fas fa-comment"></i></span>
              <span class="pl-2">{{ post.comments_count }} comments</span>
            </RouterLink>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <span class="has-text-grey is-size-7">{{ post.created_at }}</span>
          </div>
        </div>
      </nav>
    </div>

    <!-- Additional actions -->
    <div className="media-right">
      <RouterLink v-if="!showDetail" :to="{name: 'postview', params: {'id': post.id}}">
        <span class="icon"><i class="fas fa-ellipsis-vertical"></i></span>
      </RouterLink>

      <a v-else id="show-modal" @click="showModal = true">
        <span class="icon"><i class="fas fa-ellipsis-vertical"></i></span>
      </a>
    </div>
  </article>

  <Teleport v-if="showDetail" to="body">
    <!-- Delete recommendation -->
    <PostActionModal v-if="userStore.user.id === user.id" actionType="deleteAction" :show="showModal" @close="showModal = false" @submitted="deletePost">
      <template #icon>
        <i class="fas fa-trash-can fa-stack-1x has-text-white"></i>
      </template>
      <template #header>Delete recommendation</template>
      <template #body>Are you sure you want to delete this recommendation? This action cannot be undone.</template>
    </PostActionModal>

    <!-- Report recommendation -->
    <PostActionModal v-else actionType="reportAction" :show="showModal" @close="showModal = false" @submitted="reportPost">
      <template #icon>
        <i class="fa-regular fa-flag fa-stack-1x has-text-white"></i>
      </template>
      <template #header>Report recommendation</template>
      <template #body>Thank you for reporting posts that violate our community standards. Please let us know the reason for your report below and we will address the issue promptly.</template>
    </PostActionModal>
  </Teleport>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import PostActionModal from '../components/PostActionModal.vue'
import LinkCard from './LinkCard.vue'

export default {
  setup() {
    const userStore = useUserStore()

    return {
      userStore,
    }
  },
  props: {
    post: Object,
    user: Object,
    showDetail: Boolean
  },
  components: {
    RouterLink,
    PostActionModal,
    LinkCard,
  },
  data() {
    return {
      isLiked: false,
      showModal: false,
    }
  },
  mounted() {
    this.getLikes()
  },
  computed: {
    mediaClass() {
      let mediaClass = ''
      const mediaName = this.post.media_type.name

      if (mediaName == 'Television') {
        mediaClass = 'is-info'
      } else if (mediaName == 'Film') {
        mediaClass = 'is-primary'
      } else if (mediaName == 'Book') {
        mediaClass = 'is-warning'
      } else if (mediaName == 'Music') {
        mediaClass = 'is-danger'
      }

      return {
        'is-info': mediaClass == 'is-info',
        'is-primary': mediaClass == 'is-primary',
        'is-danger': mediaClass == 'is-danger',
        'is-warning': mediaClass == 'is-warning',
      }
    },
    genreClass() {
      const mediaName = this.post.media_type.name

      if (mediaName == 'Television') {
        genreClass = 'is-info'
      } else if (mediaName == 'Film') {
        genreClass = 'is-primary'
      } else if (mediaName == 'Book') {
        genreClass = 'is-warning'
      } else if (mediaName == 'Music') {
        genreClass = 'is-danger'
      }

      return {
        'is-info': genreClass == 'is-info',
        'is-primary': genreClass == 'is-primary',
        'is-danger': genreClass == 'is-danger',
        'is-warning': genreClass == 'is-warning',
      }
    },
  },
  watch: { 
    post: {
      handler: function() {
        this.getLikes()
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    getLikes() {
      axios
        .get(`/api/posts/${this.post.id}/like/`)
        .then(response => {
          const data = response.data

          if (data.likes.length > 0) {
            const user_like = data.likes.some(i => {
              return i.created_by.id === this.userStore.user.id}
            )
            this.isLiked = user_like
          } else {
            this.isLiked = false
          }
        })
        .catch(error => {
          console.error('like GET error ', error)
        })
    },
    likePost(id) {
      axios
        .post(`/api/posts/${id}/like/`)
        .then(response => {
          if (response.data.message == 'like created') {
            this.post.likes_count += 1
          }
          else {
            this.post.likes_count -= 1
          }
        })
        .catch(error => {
          console.error('like POST error ', error)
        })
    },
    deletePost() {
      axios
        .delete(`/api/posts/${this.post.id}/delete/`)
        .then(response => {
          this.$router.push('/feed')
        })
        .catch(error => {
          console.error('delete post error ', error)
        })
    },
    reportPost(body) {
      axios
        .post(`/api/posts/${this.post.id}/report/`, {
          'body': body,
          'type_of_report': 'other',
        })
        .then(response => {
          this.showModal = false
        })
        .catch(error => {
          console.error('report post error ', error)
        })
    },
  }
}
</script>