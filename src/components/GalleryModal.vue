<template>
    <div v-if="imageList && imageList.length" class="modal">
        <div class="modal-content">
            <span class="close" @click="closeModal">&times;</span>
            <h2>{{ groupName }}</h2>
            <div class="spotlight" v-if="currentImage">
                <img :src="currentImage.url" :alt="currentImage.name" class="spotlight-image" />
            </div>
            <div class="thumbnail-gallery">
                <div class="thumbnail-wrapper">
                    <img v-for="(img, index) in visibleThumbnails" :key="index" :src="img.url" :alt="img.name"
                        @click="showImage(index)" :class="{ active: currentIndex === index }" />
                </div>
            </div>
            <div class="modal-footer">
                <button @click="prevImage" v-if="imageList.length > 1">Previous</button>
                <button @click="nextImage" v-if="imageList.length > 1">Next</button>
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        imageList: Array, // Change the prop name to imageList
        groupName: String, // Keep the groupName prop as it is
    },
    data() {
        return {
            currentImage: null,
            currentIndex: 0,
            displayedThumbnails: [], // Displayed thumbnails
            thumbnailsPerPage: 20, // Number of thumbnails per page
            totalPages: 0, // Total pages for the thumbnails
            currentPage: 0, // Current page index
            visibleThumbnails: [],
        };
    },
    computed: {
        startIndex() {
            return this.currentPage * this.thumbnailsPerPage;
        },
        endIndex() {
            const endIndex = (this.currentPage + 1) * this.thumbnailsPerPage;
            return Math.min(endIndex, this.imageList.length);
        },

    },
    created() {
        this.updateVisibleThumbnails();
        this.currentImage = this.imageList[0]; // Display the first image initially
    },
    watch: {
        imageList: {
            handler(newVal) {
                if (newVal && newVal.length) {
                    this.totalPages = Math.ceil(newVal.length / this.thumbnailsPerPage);
                    this.updateVisibleThumbnails();
                } else {
                    this.totalPages = 0;
                    this.displayedThumbnails = [];
                }
            },
            immediate: true
        },
        currentIndex() {
            this.updateVisibleThumbnails();
        },
    },

    methods: {
        updateVisibleThumbnails() {
            const halfPerPage = Math.floor((this.thumbnailsPerPage - 1) / 2);
            let startIndex = this.currentIndex - halfPerPage;
            startIndex = Math.max(0, startIndex);
            const endIndex = startIndex + this.thumbnailsPerPage;

            this.visibleThumbnails = this.imageList.slice(startIndex, endIndex);

        },
        nextImage() {
            const nextIndex = (this.currentIndex + 1) % this.imageList.length;
            this.currentImage = this.imageList[nextIndex];
            this.currentIndex = nextIndex;
            this.updateVisibleThumbnails();
        },
        prevImage() {
            const prevIndex = (this.currentIndex - 1 + this.imageList.length) % this.imageList.length;
            this.currentImage = this.imageList[prevIndex];
            this.currentIndex = prevIndex;
            this.updateVisibleThumbnails();
        },
        showImage(index) {
            const halfPerPage = Math.floor((this.thumbnailsPerPage - 1) / 2);
            const newIndex = this.currentIndex - halfPerPage + index;

            if (newIndex >= 0 && newIndex < this.imageList.length) {
                this.currentIndex = newIndex;
                this.currentImage = this.imageList[newIndex];
                this.updateVisibleThumbnails();
            }
        },

        closeModal() {
            this.$emit('close-modal');
        },
    }
};
</script>
  
<style scoped>
/* Modal Styles */

.modal {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background-color: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    padding: 10px;
    border: 1px solid #888;
    border-radius: 8px;
    width: 90%;
    height: 90%;
    overflow: hidden;
    /* Ensure content doesn't overflow */
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}

.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}

.thumbnail-gallery {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 0;
    gap: 5px;
    overflow-x: auto;
    scrollbar-width: thin;
}

.thumbnail-wrapper {
    display: flex;
    gap: 5px;
    flex-wrap: nowrap;
    /* Ensure thumbnails stay in a single row */
}

.thumbnail-gallery img {
    max-width: 100px;
    height: auto;
    cursor: pointer;
}

.thumbnail-gallery img.active {
    border: 3px solid #000;
}

.spotlight {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60%;
    position: relative;
}

.spotlight img {
    max-width: 100%;
    max-height: 100%;
    margin: auto;
    display: block;
}

.modal-footer {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}

.modal-footer button {
    padding: 5px 10px;
    border: none;
    border-radius: 4px;
    background-color: #ccc;
    cursor: pointer;
}

.modal-footer button:hover {
    background-color: #ddd;
}

h2 {
    text-align: center;
    margin: 0 -2px;
}
</style>


