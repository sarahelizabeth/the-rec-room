<template>
  <div class="columns">
    <!-- Left side profile display -->
    <div class="column is-one-quarter">
      <div class="container has-text-centered mb-3">
        <div class="columns is-mobile is-centered">
          <div class="column is-full">
            <!-- Card content -->
            <div class="card">
              <!-- Avatar, name, and username -->
              <div class="card-content has-text-centered">
                <figure class="rounded-img-container-md is-inline-block">
                  <img class="rounded-img" :src="userStore.user.avatar" />
                </figure>
                <p class="title has-text-grey-dark">{{ user.name }}</p>
                <p class="subtitle is-5 has-text-grey">@{{ user.username }}</p>
              </div>
              <!-- Buttons: non-active user -->
              <div v-if="userStore.user.id !== user.id">
                <button v-if="!isFollowing" @click="follow('follow')" class="button mb-3 mr-1 is-full-width is-primary">
                  <span class="icon">
                    <i class="fas fa-user-plus"></i>
                  </span>
                  <span>Follow</span>
                </button>
                <button v-else @click="follow('unfollow')" class="button mb-3 ml-1 is-full-width is-danger">
                  <span class="icon">
                    <i class="fas fa-user-minus"></i>
                  </span>
                  <span>Unfollow</span>
                </button>
                <button @click="startChat" class="button mb-3 ml-1 is-full-width is-info">
                  <span class="icon">
                    <i class="fas fa-paper-plane"></i>
                  </span>
                  <span>Chat</span>
                </button>
              </div>
              <!-- Buttons: active user -->
              <RouterLink
                to="/profile/edit"
                v-if="userStore.user.id === user.id"
                class="button mb-3 ml-1 is-full-width is-link is-outlined"
              >
                <span class="icon">
                  <i class="fas fa-pen-to-square"></i>
                </span>
                <span>Edit</span>
              </RouterLink>
              <footer class="card-footer">
                <a
                  @click="setFollowType('followed_by')"
                  class="card-footer-item"
                  :class="[
                    { 'is-underlined': followType == 'follows' },
                    { 'has-text-weight-bold': followType == 'followed_by' },
                  ]"
                >
                  <span v-if="followed_by.length === 1">1 followers</span>
                  <span v-else>{{ followed_by.length }} followers</span>
                </a>
                <a
                  @click="setFollowType('follows')"
                  class="card-footer-item"
                  :class="[
                    { 'is-underlined': followType == 'followed_by' },
                    { 'has-text-weight-bold': followType == 'follows' },
                  ]"
                >
                  <span>{{ follows.length }} following</span>
                </a>
              </footer>
            </div>
          </div>
        </div>
      </div>
      <!-- Follows panel -->
      <Follows
        :type="followType"
        :initialSet="initialFollowSet"
        :filteredSet="followSet"
        @filterSet="filterFollowSet"
      />
    </div>

    <!-- Middle feed -->
    <div class="column">
      <!-- View filters -->
      <div v-if="userStore.user.id === user.id" class="control mb-3">
        <div class="buttons">
          <button @click.prevent="getFeed" class="button">Sent Recs</button>
          <button @click="getReceivedFeed" class="button">Received Recs</button>
          <button @click="getSavedFeed" class="button">Saved Recs</button>
        </div>
      </div>

      <!-- Posts -->
      <div v-if="posts.length > 0">
        <div v-for="post in posts" :key="post.id" class="block">
          <PostItem :post="post" :user="null" @refreshSavedFeed="getSavedFeed" />
        </div>
      </div>

      <div v-else class="content box">
        <p class="title is-size-4 secondary-text-purple">No recommendations yet!</p>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Follows from '../components/Follows.vue';
  import PostItem from '../components/PostItem.vue';

  import { useUserStore } from '@/stores/user';

  export default {
    name: 'ProfileView',
    components: {
      Follows,
      PostItem,
    },
    setup() {
      const userStore = useUserStore();
      return {
        userStore,
      };
    },
    data() {
      return {
        posts: [],
        user: {},
        isFollowing: false,
        follows: [],
        followed_by: [],
        followType: 'followed_by',
        followSet: [],
        initialFollowSet: [],
      };
    },
    mounted() {
      this.getFeed();
      this.getFollows();
    },
    watch: {
      '$route.params.id': {
        handler: function () {
          this.getFeed();
          this.getFollows();
        },
        deep: true,
        immediate: true,
      },
      isFollowing: {
        handler: function () {
          this.getFollows();
        },
        deep: true,
        immediate: true,
      },
    },
    methods: {
      getFeed() {
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/`)
          .then((response) => {
            this.posts = response.data.posts;
            this.user = response.data.user;
          })
          .catch((error) => {
            console.error('feed GET error ', error);
          });
      },
      getReceivedFeed() {
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/received/`)
          .then((response) => {
            this.posts = response.data.posts;
            this.user = response.data.user;
          })
          .catch((error) => {
            console.error('received GET error ', error);
          });
      },
      getSavedFeed() {
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/saved/`)
          .then((response) => {
            this.posts = response.data.posts;
            this.user = response.data.user;
          })
          .catch((error) => {
            console.error('saved GET error ', error);
          });
      },
      getFollows() {
        axios
          .get(`/api/${this.$route.params.id}/get-follows/`)
          .then((response) => {
            const user = response.data.user;
            const profile = response.data.profile;

            this.follows = profile.follows;
            this.followed_by = profile.followed_by;
            this.initialFollowSet = profile.followed_by;
            this.followSet = profile.followed_by;
            this.isFollowing = user.follows.some((el) => el.id === profile.id);
          })
          .catch((error) => {
            console.error('get follows error ', error);
          });
      },
      filterFollowSet(filtered) {
        this.followSet = filtered;
      },
      setFollowType(type) {
        this.followType = type;

        if (this.followType == 'follows') {
          this.initialFollowSet = this.follows;
          this.followSet = this.follows;
        } else {
          this.initialFollowSet = this.followed_by;
          this.followSet = this.followed_by;
        }
      },
      startChat() {
        axios
          .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
          .then((response) => {
            console.log('start chat response ', response.data);
            this.$router.push(`/chat/${response.data.id}/`);
          })
          .catch((error) => {
            console.error('start chat error ', error);
          });
      },
      follow(type) {
        axios
          .post(`/api/${this.$route.params.id}/follow/`, {
            followType: type,
          })
          .then((response) => {
            if (response.data.message === 'followed') {
              this.isFollowing = true;
            } else {
              this.isFollowing = false;
            }
          })
          .catch((error) => {
            console.error('follow error ', error);
          });
      },
    },
  };
</script>
