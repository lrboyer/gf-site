<template>
  <div class="main">
    <Navbar />
    <div class="upload">
      <Upload />
    </div>
    <button class="submit-button" @click="refreshImages">Refresh Images</button>
    <div class="list">
      <ImageGroup v-for="(imageGroup, index) in imageData" :key="imageGroup.group" :groupName="imageGroup.group"
        :imageList="imageGroup.images" :index="index" @group-selected="filterImagesByGroup" />
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
import Navbar from '../components/Navbar.vue';

export default {
  components: {
    Navbar,
    ImageGroup,
    GalleryModal,
    Upload,
  },
  data() {
    return {
      apiUrl: "https://jwxchy0pkl.execute-api.us-east-1.amazonaws.com",
      groups: [],
      imageData: [],
      showModal: false,
      selectedGroup: null,
      selectedGroupImages: [],
    };
  },
  created() {
    this.fetchGroups();
  },
  methods: {
    async fetchGroups() {
      try {
        const response = await axios.get(`${this.apiUrl}/images`);
        this.groups = response.data;
        console.log(response.data)
        for (let i = 0; i < this.groups.length; i++) {
          await this.fetchImageData(this.groups[i]);
        }
      } catch (error) {
        console.error('Error fetching group data:', error);
      }
    },
    async fetchImageData(group) {
      try {
        const response = await axios.get(`${this.apiUrl}/images/${group}`);

        if (response.data) {
          const imagesData = {
            group: response.data.group,
            images: response.data.images,
          };

          this.imageData.push(imagesData)
        }
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
    refreshImages() {
      // Clear existing data and fetch again
      this.imageData = [];
      this.groups = []
      this.fetchGroups();
    },
  },
};
</script>

<style scoped>
div .main {
  background: url('../images/sanrio-background.jpg');
  background-repeat: repeat;
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

.upload {
  margin-top: 75px;
}

.submit-button {
  margin: 10px;
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>
