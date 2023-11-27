<template>
  <div class="main">
    <div class="list">
      <ImageGroup v-for="imageGroup in imageData" :key="imageGroup.group" :groupName="imageGroup.group"
        :groupColor="groupColor">
        <img v-for="img in imageGroup.imgs" :key="img.name" :src="img.url" :alt="img.name" />
      </ImageGroup>
    </div>
  </div>
</template>

<script>
import ImageGroup from '../components/ImageGroup.vue'
import imageData from '@/data/image-data.json';

export default {
  components: {
    ImageGroup,
  },
  data() {
    return {
      groupColor: 'beige', // Define your group color here
      imageData: {
        images: [],
      },
    };
  },
  created() {
    this.imageData = imageData.data; // Assign the 'data' array to imageData
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
