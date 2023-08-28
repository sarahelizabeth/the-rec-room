import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import ProfileView from '../views/ProfileView.vue'
import PostView from '../views/PostView.vue'
import ChatView from '../views/ChatView.vue'
import TrendView from '../views/TrendView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import MediaTypeView from '../views/MediaTypeView.vue'
import NotificationsView from '../views/NotificationsView.vue'

const routes = [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/profile/edit',
      name: 'editprofile',
      component: EditProfileView
    },
    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/trends/:id',
      name: 'trend',
      component: TrendView
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView
    },
    {
      path: '/media-type/:id',
      name: 'mediatype',
      component: MediaTypeView,
      props: true,
    },
  ]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export default router