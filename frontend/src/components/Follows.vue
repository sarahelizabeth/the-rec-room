<template>
  <article class="panel">
    <p class="panel-heading">
      <span v-if="type == 'follows'">Following</span>
      <span v-else>Followers</span>
      <!-- Hiding this on mobile until search works correctly -->
      <span class="icon is-right is-hidden-mobile">
        <a v-if="showSearch" @click.prevent="toggleSearch"><i class="fas fa-xmark" aria-hidden="true"></i></a>
        <a v-else @click.prevent="toggleSearch"><i class="fas fa-search" aria-hidden="true"></i></a>
      </span>
    </p>
    <!-- hiding this on mobile until search works correctly -->
    <div v-if="showSearch" class="panel-block is-hidden-mobile">
      <p class="control has-icons-left">
        <input v-model.trim="searchInput" class="input" type="text" placeholder="Search..." />
        <span class="icon is-left">
          <i class="fas fa-search" aria-hidden="true"></i>
        </span>
      </p>
    </div>
    <div v-for="follow in filteredSet" :key="follow.id">
      <RouterLink :to="{ name: 'profile', params: { id: follow.id } }" class="panel-block is-active">
        <span class="panel-icon">
          <i class="fas fa-user" aria-hidden="true"></i>
        </span>
        {{ follow.name }}
      </RouterLink>
    </div>
  </article>
</template>

<script>
  import { RouterLink } from 'vue-router';
  import { useUserStore } from '@/stores/user';

  export default {
    name: 'Follows',
    setup() {
      const userStore = useUserStore();
      return {
        userStore,
      };
    },
    data() {
      return {
        showSearch: false,
        searchInput: '',
      };
    },
    props: {
      user: Object,
      type: String,
      filteredSet: Array,
      initialSet: Array,
    },
    components: {
      RouterLink,
    },
    watch: {
      searchInput(query) {
        const filteredArr = this.initialSet.filter((el) => {
          return el.name.toLowerCase().includes(query) || el.username.toLowerCase().includes(query);
        });
        this.$emit('filterSet', filteredArr);
      },
    },
    methods: {
      toggleSearch() {
        this.showSearch = !this.showSearch;
      },
    },
  };
</script>

<style scoped>
  .panel-heading {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
</style>
