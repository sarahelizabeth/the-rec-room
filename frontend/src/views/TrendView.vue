<template>
  <div class="columns">
    <!-- Trend feed container -->
    <div class="column is-two-thirds">
      <div class="box p-3">
        <p class="is-size-4 has-text-weight-bold primary-text-purple">#{{ $route.params.id }}</p>
      </div>

      <!-- All posts -->
      <div v-for="post in posts" :key="post.id" class="block">
        <PostItem :post="post" :showDescription="true" />
      </div>
    </div>

    <!-- Right side tags and navigation -->
    <div class="column is-one-third">
      <!-- <MediaTypes /> -->
      <Trends />
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Follows from '../components/Follows.vue';
  import Trends from '../components/Trends.vue';
  import MediaTypes from '../components/MediaTypes.vue';
  import PostItem from '../components/PostItem.vue';
  import { useUserStore } from '@/stores/user';

  export default {
    name: 'TrendView',
    components: {
      Follows,
      Trends,
      MediaTypes,
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
        body: '',
      };
    },
    mounted() {
      this.getFeed();
    },
    watch: {
      '$route.params.id': {
        handler: function () {
          this.getFeed();
        },
        deep: true,
        immediate: true,
      },
    },
    methods: {
      getFeed() {
        axios
          .get(`/api/posts/?trend=${this.$route.params.id}`)
          .then((response) => {
            this.posts = response.data;
          })
          .catch((error) => {
            console.error('trends GET error ', error);
          });
      },
    },
  };
</script>
