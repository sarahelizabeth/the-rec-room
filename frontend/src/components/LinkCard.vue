<template>
  <article class="media p-0" id="linkCardContainer">
    <figure class="media-left m-0">
      <a :href="link" id="linkImgContainer" class="image" target="_blank">
        <img id="linkImg" v-if="!loading" :src="linkData?.images[0]">
      </a>
    </figure>
    <div class="media-content">
      <div v-if="loading" class="p-5 m-5">
          <div class="loader"></div>
      </div>
      <div v-else class="p-3">
        <p class="is-size-6 mb-2">{{ linkData?.title }}</p>
        <p class="is-size-7">{{ linkDescription }}</p>
      </div>
    </div>
    <!-- <div class="media-right p-3">
      <button class="delete"></button>
    </div> -->
  </article>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'

export default {
  props: {
    link: String
  },
  data() {
    return {
      linkData: '',
      loading: true,
    }
  },
  mounted() {
    this.getMetadata()
  },
  computed: {
    linkDescription() {
      return this.linkData?.description?.length < 130 ? this.linkData?.description : this.linkData?.description?.substring(0, 130) + '...'
    }
  },
  methods: {
    getMetadata() {
      let newLink = 'https://bulma.io/images/placeholders/128x128.png'
      if (this.link && typeof (this.link) !== 'undefined' && this.link !== null) {
        newLink = this.link
      }
      axios
        .get(`https://jsonlink.io/api/extract?url=${newLink}`)
        .then(response => {
          this.linkData = response.data
        })
        .then(() => this.loading = false)
        .catch(error => console.error('get link data error ', error))
    },
    imgSize() {
      let img = document.querySelector("#linkImg");
      let width = img.naturalWidth;
      let height = img.naturalHeight;
      console.log("Original width=" + width + ", " + "Original height=" + height);
    }
  },
  components: { RouterLink }
}
</script>

<style>
#linkCardContainer {
  border: 1px solid #625AD8;
  border-radius: 20px;
}
#linkImg {
  max-width: 100%; 
  max-height: 100%; 
  vertical-align: bottom;
  width: inherit;
  height: inherit;
  border-radius: inherit;
  object-fit: cover;
  object-position: center;
  border-radius: 20px 0 0 20px;
}
#linkImgContainer {
  width: 128px;
  height: 128px;
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  border-radius: 20px 0 0 20px;
}
</style>