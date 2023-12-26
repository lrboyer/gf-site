<template>
    <div class="page">
        <Navbar />
        <div class="body">
            <div v-if="showGif" class="enter-gif">
                <form class="login-form">
                    <img src="https://media.giphy.com/media/FTGah7Mx3ss04PcasF/giphy.gif">
                    <h1>Do you want to see literally us?</h1>
                    <button @click="showForm" class="submit-button">Yes</button>
                </form>
            </div>
            <div v-else>
                <form @submit.prevent="handleSubmit" class="login-form">
                    <img src="https://media.giphy.com/media/UMon0fuimoAN9ueUNP/giphy.gif">
                    <h1>LB X LR Relationship Timeline</h1>
                    <input v-model="formData" placeholder="Enter password" type="password" class="input-field">
                    <button type="submit" class="submit-button">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>
  
<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from '../components/Navbar.vue';

export default {
    setup() {
        const formData = ref('');
        const showGif = ref(true);
        const correctPassword = '12345';
        const router = useRouter();
        const showForm = () => {
            showGif.value = false;
        };
        const handleSubmit = () => {
            if (formData.value === correctPassword) {
                router.push('/LB-X-LR-LITERALLY-US-TIMELINE');
            }
            else {
                alert('Incorrect password. Please try again.');
                formData.value = '';
            }
        };
        return { formData, showGif, showForm, handleSubmit };
    },
    components: { Navbar }
};
</script>

  
<style scoped>
.page {
    background-image: url('../images/sanrio-background.jpg');
    background-size: repeat;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.body {
    min-height: 98vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.login-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.input-field {
    margin-bottom: 15px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 200px;
    font-size: 16px;
}

.submit-button {
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

.enter-gif {
    /* Styles for the GIF container */
    display: flex;
    flex-direction: column;
    align-items: center;
    /* Add other styles as needed */
}

.no-button {
    /* Styles for the No button */
    cursor: pointer;
    transition: transform 0.3s ease;
}

.no-button:hover {
    transform: scale(1.1);
    /* Example transformation on hover */
}
</style>
  