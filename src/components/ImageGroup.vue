<template>
    <div class="group">
        <h2>{{ groupName }}</h2>
        <div class="images" @click="selectGroup">
            <img v-for="img in imageList" :key="img.name" :src="img.url" :alt="img.name" />
        </div>
    </div>
</template>
  
<script>
export default {
    methods: {
        selectGroup() {
            if (this.imageList && this.imageList.length > 0) {
                this.$emit('group-selected', this.groupName);
            }
        }
    },
    props: {
        groupName: String,
        imageList: Array,
    },
};
</script>
  
<style scoped>
.group {
    margin-bottom: 20px;
    padding: 20px;
    border-radius: 8px;
    background-color: burlywood;
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
  