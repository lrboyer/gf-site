<template>
  <div class="main">
    <Upload />
    <div class="list">
      <ImageGroup v-for="imageGroup in imageData" :key="imageGroup.group" :groupName="imageGroup.group"
        :imageList="imageGroup.images" @group-selected="filterImagesByGroup" />
    </div>
    <GalleryModal v-if="showModal" :groupName="selectedGroup.group" :imageList="selectedGroupImages"
      @close-modal="closeModal" />
  </div>
</template>

<script>
import ImageGroup from '../components/ImageGroup.vue'
import GalleryModal from '../components/GalleryModal.vue'
import Upload from '../components/Upload.vue'
import axios from 'axios';

export default {
  components: {
    ImageGroup,
    GalleryModal,
    Upload,
  },
  data() {
    return {
      apiUrl: "https://jwxchy0pkl.execute-api.us-east-1.amazonaws.com",
      imageData: [],
      showModal: false,
      selectedGroup: null,
      selectedGroupImages: [],
    };
  },
  created() {
    this.fetchImageData();
  },
  methods: {
    async fetchImageData() {
      try {
        const response = await axios.get(`${this.apiUrl}/images`);
        this.imageData = response.data;
      } catch (error) {
        console.error('Error fetching image data:', error);
      }
    },
    filterImagesByGroup(groupName) {
      // Find the selected group data
      this.selectedGroup = this.imageData.find(group => group.group === groupName);

      // Update filtered images to show only images in the selected group
      if (this.selectedGroup) {
        this.selectedGroupImages = this.selectedGroup.images; // Store selected group images
        this.showModal = true; // Open the modal
      }
    },
    closeModal() {
      this.showModal = false; // Close the modal
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
</style>
