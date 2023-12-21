<template>
    <div>
        <input v-model="groupName" placeholder="Enter group name" class="input-field">
        <button @click="openFileInput">Upload</button>
        <input ref="fileInput" type="file" style="display: none" multiple accept="image/*" @change="handleFileChange" />
    </div>
</template>
  
<script>
import axios from 'axios';

const apiUrl = "https://jwxchy0pkl.execute-api.us-east-1.amazonaws.com"

export default {
    data() {
        return {
            groupName: '',
            files: [],
        };
    },
    methods: {
        openFileInput() {
            this.$refs.fileInput.click();
        },
        async handleFileChange(event) {
            const files = event.target.files;

            // Iterate through each file and initiate the upload
            for (let i = 0; i < files.length; i++) {
                let file = files[i]
                const presignedUrl = await this.getPresignedUrl(file.name);
                await this.uploadFile(file, presignedUrl);
            }
            console.log("SUCESSFULLY UPLOADED ALL IMAGES")
        },
        async getPresignedUrl(fileName) {
            try {
                const response = await axios.get(`${apiUrl}/upload?fileName=${encodeURIComponent(fileName)}&groupName=${encodeURIComponent(this.groupName)}`);
                let url = response.data.presignedUrl

                return url
            } catch (error) {
                console.error('Error getting presigned URL:', error);
                throw new Error('Failed to get presigned URL');
            }
        },
        async uploadFile(file, presignedUrl) {
            try {
                // Use the presigned URL to upload the file directly to S3 using Axios
                const options = {
                    headers: {
                        'Content-Type': 'image/*',
                    },
                };

                await axios.put(presignedUrl, file, options);
            } catch (error) {
                console.error('Error uploading file:', error);
                throw new Error('Failed to upload file');
            }
        },
    },
};
</script>
  
<style scoped></style>