<template>
    <div class="group">
        <h1>{{ groupName }}</h1>
        <div class="images">
            <slot></slot>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        groupName: String
    },
};
</script>
  
<style scoped>
.group {
    margin-bottom: 20px;
    padding: 20px;
    border-radius: 8px;
}

.images {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    grid-auto-flow: dense;
    grid-gap: 10px;
    background-color: burlywood;
}
</style>
  