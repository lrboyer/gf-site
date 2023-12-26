<template>
    <div class="upload-form">
        <button class="drawer-button" @click="toggleDrawer">Image Upload / Instructions</button>

        <div v-show="isDrawerOpen">
            <div class="text-group">
                <h1>How to upload</h1>
                <h3>
                    1. To add a new group
                </h3>
                <p>a. Enter a unique group name</p>
                <p>b. Hit select images, then choose all images to add to group</p>
                <p>c. Hit upload, then a popup saying it worked should appear</p>
                <p>d. Hit refresh images</p>

                <h3>
                    2. Add onto existing group
                </h3>
                <p>a. Type in the exact group name you want to add onto</p>
                <p>b. Upload as usual </p>
            </div>

            <div class="form-group">
                <h1>Upload</h1>
                <label for="groupName">Group Name:</label>
                <input v-model="groupName" id="groupName" class="input-field" placeholder="Enter group name">
            </div>

            <div class="form-group">
                <label class="upload-label">Select Image(s):</label>
                <button class="upload-button" @click="openFileInput">Choose File(s)</button>
                <input ref="fileInput" type="file" style="display: none" multiple accept="image/*"
                    @change="handleFileChange" />
            </div>

            <div class="submit-group">
                <button class="submit-button" @click="uploadImages">Upload</button>
            </div>
        </div>
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
            isDrawerOpen: false,
        };
    },
    methods: {
        openFileInput() {
            this.$refs.fileInput.click();
        },
        async handleFileChange(event) {
            this.files = event.target.files;
        },
        async uploadImages() {
            for (let i = 0; i < this.files.length; i++) {
                const file = this.files[i];
                const presignedUrl = await this.getPresignedUrl(file.name);
                await this.uploadFile(file, presignedUrl);
            }
            window.alert("SUCCESSFULLY UPLOADED ALL IMAGES");
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
        toggleDrawer() {
            this.isDrawerOpen = !this.isDrawerOpen;
        },
    },
};
</script>
  
<style scoped>
.drawer-button {
    padding: 8px 12px;
    margin-bottom: 10px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    font-size: 14px;
    cursor: pointer;
}

.text-group {
    margin: 20px;
}

.submit-group {
    margin: 20px;
    display: flex;
    justify-content: center;
}

.submit-button {
    padding: 10px 22px;
    border: none;
    border-radius: 4px;
    background-color: #ff0000;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.submit-button:hover {
    background-color: #a22a2a;
}

.upload-form {
    display: flex;
    flex-direction: column;
    width: 400px;
    margin: 0 auto;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin: 20px;
}

.input-field {
    width: 80%;
    margin-top: 5px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.upload-label {
    display: block;
    margin-bottom: 8px;
}

.upload-button {
    padding: 8px 12px;
    margin: 20px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.upload-button:hover {
    background-color: #0056b3;
}
</style>