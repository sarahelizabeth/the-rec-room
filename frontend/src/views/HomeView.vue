<script setup></script>

<template>
  <div class="column is-half is-offset-one-quarter is-full-mobile">
    <div class="box content" style="border: 2px solid #964ec2">
      <a
        href="https://www.youtube.com/watch?v=WB8XDk3sQBc"
        target="_blank"
        class="primary-text-purple has-text-weight-bold is-size-4"
      >
        Don't Panic! <i class="fas fa-user-astronaut ml-1"></i>
      </a>
      <p class="mt-3">
        If you're reading this, that means Sarah has roped you into testing her awesome app! Once you've created an
        account, you will join the tens of other users of
        <strong class="primary-text-purple has-text-weight-bold">The Rec Room</strong>: a movie, TV, music, and book
        recommendation app in which you will be able to create trends, chat with other users, and—of course—pester your
        friends, loved ones, and enemies with recs for all your favorite media.
      </p>
      <!-- Buttons for mobile -->
      <div class="field is-grouped is-grouped-centered mt-3 is-hidden-tablet is-hidden-destop is-hidden-fullscreen">
        <!-- <div v-if="userStore.user.isAuthenticated">
          <div class="control">
            <RouterLink :to="{ name: 'feed' }" class="button is-secondary-purple has-text-white">
              <strong>Feed</strong>
            </RouterLink>
          </div>
          <div class="control">
            <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }" @click.native="closeNav">
              Profile
            </RouterLink>
          </div>
        </div> -->
        <!-- <div v-else> -->
        <div class="control">
          <RouterLink :to="{ name: 'signup' }" class="button is-secondary-purple has-text-white">
            <strong>Sign up</strong>
          </RouterLink>
        </div>
        <div class="control">
          <RouterLink :to="{ name: 'login' }" class="button is-outlined"> Log in </RouterLink>
        </div>
        <!-- </div> -->
      </div>
    </div>
  </div>
</template>
