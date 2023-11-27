<template>
    <div>
        <form @submit.prevent="handleSubmit" class="login-form">
            <h1>LL Relationship Timeline</h1>
            <input v-model="formData" placeholder="Enter password" type="password" class="input-field">
            <button type="submit" class="submit-button">Submit</button>
        </form>
    </div>
</template>
  
<script setup>
import { useRouter } from 'vue-router';

let formData = '';
const correctPassword = '12345';

const router = useRouter();

const handleSubmit = () => {
    if (formData === correctPassword) {
        router.push('/timeline');
    } else {
        alert('Incorrect password. Please try again.');
        formData = '';
    }
};
</script>
  
<style scoped>
div {
    background-image: url('../images/sanrio-background.jpg');
    background-size: cover;
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
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
</style>
  