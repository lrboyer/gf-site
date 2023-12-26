<template>
    <div class="group" :style="{ backgroundColor: groupColor }">
        <h2>{{ groupName }}</h2>
        <div class="images" @click="selectGroup">
            <img v-for="img in imageList" :key="img.name" :src="img.url" :alt="img.name" />
        </div>
    </div>
</template>

  
<script>
const rainbowColors = [
    '#FFB6C1', '#FFD700', '#FFECB3', '#98FB98', '#ADD8E6', '#E6E6FA', '#F0E68C'
];
export default {
    methods: {
        selectGroup() {
            if (this.imageList && this.imageList.length > 0) {
                this.$emit('group-selected', this.groupName);
            }
        },
    },
    props: {
        groupName: String,
        imageList: Array,
        index: Number
    },
    data() {
        return {
            colorIndex: this.index,
        };
    },
    computed: {
        groupColor() {
            return rainbowColors[this.colorIndex];
        },
    },
    created() {
        // Increment colorIndex when a new group is created
        this.colorIndex = (this.colorIndex + 1) % rainbowColors.length;
    },
}
</script>
  
<style scoped>
.group {
    margin-bottom: 20px;
    padding: 20px;
    border-radius: 8px;
}

img {
    width: 100%;
    height: auto;
}

.images {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    grid-auto-flow: dense;
    grid-gap: 10px;
}
</style>
  