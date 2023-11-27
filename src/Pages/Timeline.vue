<template>
  <div class="main">
    <div class="list">
      <ImageGroup v-for="imageGroup in imageData" :key="imageGroup.group" :groupName="imageGroup.group">
        <img v-for="img in imageGroup.images" :key="img.name" :src="img.url" :alt="img.name" />
      </ImageGroup>
    </div>
  </div>
</template>

<script>
import ImageGroup from '../components/ImageGroup.vue'
import axios from 'axios';

export default {
  components: {
    ImageGroup,
  },
  data() {
    return {
      imageData: [],
    };
  },
  created() {
    this.fetchImageData();
  },
  methods: {
    async fetchImageData() {
      try {
        const response = await axios.get('https://pqlubejjk8.execute-api.us-east-1.amazonaws.com/dev/images');
        this.imageData = JSON.parse(response.data.body);
      } catch (error) {
        console.error('Error fetching image data:', error);
      }
    },
  },
};
</script>

<style scoped>
div .main {
  background-image: url('../images/sanrio-background.jpg');
  background-size: cover;
  width: 100%;
  height: 100%;
  min-width: 100vw;
  min-height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.list {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.75);
  width: 75%;
  height: 100%;
}

img {
  width: 100%;
  height: auto;
}
</style>
