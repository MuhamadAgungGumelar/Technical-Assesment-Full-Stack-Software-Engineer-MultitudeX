<script setup>
import { ref, defineEmits } from "vue";
import axios from "axios";

const emits = defineEmits(["usernameSubmitted"]);

const username = ref(null); // Variable to hold username
const message = ref(""); // Error or success message

async function submitUsername() {
  try {
    const response = await axios.post(
      "http://localhost:8000/username/",
      { username: username.value }, // Send username to backend
      { withCredentials: true } // Use credentials for authorization
    );
    console.log(response.data); // Log response from backend
    // Store user_id in local storage after successful submission
    localStorage.setItem("user_id", response.data.id);

    message.value = "Username submitted successfully!"; // Set success message
    emits("usernameSubmitted"); // Emit event when username is submitted
  } catch (error) {
    console.error("Failed to submit username:", error); // Log error if submission fails
    message.value = "Failed to submit username."; // Set error message
  }
}
</script>

<template>
  <div class="flex flex-col gap-5">
    <div v-if="message" role="alert" class="alert alert-error text-white">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 shrink-0 stroke-current"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <p>{{ message }}</p>
    </div>
    <label class="input input-bordered flex items-center gap-2">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 16 16"
        fill="currentColor"
        class="h-4 w-4 opacity-70"
      >
        <path
          d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z"
        />
      </svg>
      <input
        v-model="username"
        type="text"
        class="grow"
        placeholder="Enter Your Username"
      />
    </label>
    <button @click="submitUsername" class="btn btn-outline w-24">Submit</button>
  </div>
</template>
