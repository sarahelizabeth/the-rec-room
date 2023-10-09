<template>
  <article class="media box">
    <!-- Profile image -->
    <figure class="media-left is-hidden-mobile">
      <div class="rounded-img-container-sm">
        <img class="rounded-img" :src="post.created_by.get_avatar" />
      </div>
    </figure>

    <!-- Rec title -->
    <div class="media-content">
      <div class="content">
        <span>
          <strong>
            <RouterLink :to="{ name: 'profile', params: { id: post.created_by.id } }">{{
              post.created_by.name
            }}</RouterLink>
          </strong>
          recommended
          <strong>{{ post.title }}</strong>
          <span v-if="post.recipients?.length > 0">
            <!-- to <strong>{{ post.recipients.map(e => e.name).join(', ')}}</strong> -->
            to
            <strong v-for="(recipient, index) in post.recipients">
              <RouterLink :to="{ name: 'profile', params: { id: recipient.id } }">{{ recipient.name }}</RouterLink>
              <span v-if="index < post.recipients.length - 1">, </span>
            </strong>
          </span>
        </span>

        <!-- Genres -->
        <div class="py-1">
          <span :class="mediaClass" class="tag mr-2">{{ post.media_type.name }}</span>
          <span v-for="genre in post.genres" :class="mediaClass" class="tag is-light mr-2">{{ genre.name }}</span>
        </div>

        <!-- Rec detail -->
        <div v-if="showDetail || showDescription">
          <span v-if="!isEditing">{{ post.body }}</span>
          <div v-else class="control">
            <div class="field">
              <textarea class="textarea" rows="4" v-model="post.body" placeholder="A short description..."></textarea>
            </div>
            <div class="field">
              <div class="buttons is-right">
                <button @click="toggleEdit" class="button is-small is-danger is-outlined">Cancel</button>
                <button @click="saveDetail" class="button is-small is-link is-outlined">
                  <span class="icon">
                    <i class="fas fa-floppy-disk"></i>
                  </span>
                  <span>Save</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Link card -->
        <LinkCard v-if="showDetail && post.link" :link="post.link" class="my-4 is-hidden-mobile" />
      </div>

      <!-- Bottom elements -->
      <nav class="level is-mobile">
        <div class="level-left">
          <div class="level-item" @click="likePost(post.id)">
            <a :class="{ 'has-text-danger': isLiked, 'has-text-grey': !isLiked }" class="icon is-small"
              ><i class="fas fa-heart"></i
            ></a>
            <span v-if="post.likes_count === 1" class="pl-2">{{ post.likes_count }} like</span>
            <span v-else class="pl-2">{{ post.likes_count }} likes</span>
          </div>
          <div class="level-item">
            <RouterLink :to="{ name: 'postview', params: { id: post.id } }">
              <span class="icon is-small"><i class="fas fa-comment"></i></span>
              <span v-if="post.comments_count === 1" class="pl-2">{{ post.comments_count }} comment</span>
              <span v-else class="pl-2">{{ post.comments_count }} comments</span>
            </RouterLink>
          </div>
          <div v-if="userStore.user.id !== post.created_by.id" class="level-item" @click="savePost(post.id)">
            <a :class="{ 'has-text-warning': isSaved, 'has-text-grey': !isSaved }" class="icon is-small"
              ><i class="fas fa-star"></i
            ></a>
            <span v-if="post.saves_count === 1" class="pl-2">{{ post.saves_count }} save</span>
            <span v-else class="pl-2">{{ post.saves_count }} saves</span>
          </div>
          <!-- <div class="level-item" @click="likePost(post.id)">
            <a :class="{'has-text-success': !isWatched, 'has-text-grey': isWatched}" class="icon is-small"><i class="fas fa-solid fa-circle-check"></i></a>
            <span class="pl-2">watched</span>
          </div> -->
        </div>
        <div class="level-right is-hidden-mobile">
          <div class="level-item">
            <span class="has-text-grey is-size-7">{{ post.created_at }}</span>
          </div>
        </div>
      </nav>
    </div>

    <!-- Post actions -->
    <div className="media-right">
      <!-- Go to post detail view -->
      <RouterLink v-if="!showDetail" :to="{ name: 'postview', params: { id: post.id } }">
        <span class="icon"><i class="fas fa-ellipsis-vertical"></i></span>
      </RouterLink>

      <div v-else>
        <!-- Report -->
        <div v-if="userStore.user.id !== user.id">
          <a id="show-modal" @click="showModal = true">
            <span class="icon"><i class="fas fa-ellipsis-vertical"></i></span>
          </a>
        </div>

        <!-- Additional actions -->
        <div v-else :class="{ 'is-active': showDropdown }" class="dropdown is-right">
          <a @click="showDropdown = !showDropdown" class="dropdown-trigger">
            <span class="icon"><i class="fas fa-ellipsis-vertical"></i></span>
          </a>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a @click="toggleEdit" class="dropdown-item"> Edit Rec </a>
              <a class="dropdown-item"> Add Recipients </a>
              <a id="show-modal" @click="showModal = true" class="dropdown-item has-text-danger"> Delete </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </article>

  <Teleport v-if="showDetail" to="body">
    <!-- Delete recommendation -->
    <PostActionModal
      v-if="userStore.user.id === user.id"
      actionType="deleteAction"
      :show="showModal"
      @close="showModal = false"
      @submitted="deletePost"
    >
      <template #icon>
        <i class="fas fa-trash-can fa-stack-1x has-text-white"></i>
      </template>
      <template #header>Delete recommendation</template>
      <template #body>Are you sure you want to delete this recommendation? This action cannot be undone.</template>
    </PostActionModal>

    <!-- Report recommendation -->
    <PostActionModal
      v-else
      actionType="reportAction"
      :show="showModal"
      @close="showModal = false"
      @submitted="reportPost"
    >
      <template #icon>
        <i class="fa-regular fa-flag fa-stack-1x has-text-white"></i>
      </template>
      <template #header>Report recommendation</template>
      <template #body
        >Thank you for reporting posts that violate our community standards. Please let us know the reason for your
        report below and we will address the issue promptly.</template
      >
    </PostActionModal>
  </Teleport>
</template>

<script>
  import axios from 'axios';
  import { RouterLink } from 'vue-router';
  import { useUserStore } from '@/stores/user';
  import PostActionModal from '../components/PostActionModal.vue';
  import LinkCard from './LinkCard.vue';

  export default {
    setup() {
      const userStore = useUserStore();

      return {
        userStore,
      };
    },
    props: {
      post: Object,
      user: Object,
      showDetail: Boolean,
      showDescription: Boolean,
    },
    components: {
      RouterLink,
      PostActionModal,
      LinkCard,
    },
    data() {
      return {
        isLiked: false,
        isSaved: false,
        showDropdown: false,
        isEditing: false,
        showModal: false,
      };
    },
    mounted() {
      this.getLikes();
      this.getSavedRecs();
    },
    computed: {
      mediaClass() {
        let mediaClass = '';
        const mediaName = this.post.media_type.name;

        if (mediaName == 'Television') {
          mediaClass = 'is-info';
        } else if (mediaName == 'Film') {
          mediaClass = 'is-primary';
        } else if (mediaName == 'Book') {
          mediaClass = 'is-warning';
        } else if (mediaName == 'Music') {
          mediaClass = 'is-danger';
        }

        return {
          'is-info': mediaClass == 'is-info',
          'is-primary': mediaClass == 'is-primary',
          'is-danger': mediaClass == 'is-danger',
          'is-warning': mediaClass == 'is-warning',
        };
      },
    },
    watch: {
      post: {
        handler: function () {
          this.getLikes();
          this.getSavedRecs();
        },
        deep: true,
        immediate: true,
      },
    },
    emits: ['refreshSavedFeed'],
    methods: {
      getLikes() {
        axios
          .get(`/api/posts/${this.post.id}/like/`)
          .then((response) => {
            if (response.data.likes.length > 0) {
              const user_like = response.data.likes.some((i) => {
                return i.created_by.id === this.userStore.user.id;
              });
              this.isLiked = user_like;
            } else {
              this.isLiked = false;
            }
          })
          .catch((error) => {
            console.error('like GET error ', error);
          });
      },
      getSavedRecs() {
        axios
          .get(`/api/posts/${this.post.id}/save/`)
          .then((response) => {
            if (response.data.saved_recs.length > 0) {
              const user_save = response.data.saved_recs.some((i) => {
                return i.created_by.id === this.userStore.user.id;
              });
              this.isSaved = user_save;
            } else {
              this.isSaved = false;
            }
          })
          .catch((error) => {
            console.error('save GET error ', error);
          });
      },
      likePost(id) {
        axios
          .post(`/api/posts/${id}/like/`)
          .then((response) => {
            if (response.data.message == 'like created') {
              this.post.likes_count += 1;
            } else {
              this.post.likes_count -= 1;
            }
          })
          .catch((error) => {
            console.error('like POST error ', error);
          });
      },
      savePost(id) {
        axios
          .post(`/api/posts/${id}/save/`)
          .then((response) => {
            if (response.data.message == 'post saved') {
              this.post.saves_count += 1;
            } else {
              this.post.saves_count -= 1;
              this.$emit('refreshSavedFeed');
            }
          })
          .catch((error) => {
            console.error('save POST error ', error);
          });
      },
      toggleEdit() {
        this.isEditing = !this.isEditing;
        this.showDropdown = false;
      },
      saveDetail() {
        axios
          .post(`/api/posts/${this.post.id}/edit/`, {
            body: this.post.body,
          })
          .then(() => {
            this.isEditing = false;
          })
          .catch((error) => {
            console.error('save detail post error ', error);
            this.isEditing = false;
          });
      },
      deletePost() {
        axios
          .delete(`/api/posts/${this.post.id}/delete/`)
          .then(() => {
            this.$router.push('/feed');
          })
          .catch((error) => {
            console.error('delete post error ', error);
          });
      },
      reportPost(body) {
        axios
          .post(`/api/posts/${this.post.id}/report/`, {
            body: body,
            type_of_report: 'other',
          })
          .then(() => {
            this.showModal = false;
          })
          .catch((error) => {
            console.error('report post error ', error);
          });
      },
    },
  };
</script>
