<script setup>
import { ref } from "vue";
import FeedBack from "./FeedBack.vue";
import Username from "./Username.vue";

const modalVisible = ref(false); // Modal visibility status
const showUsernameForm = ref(true); // Username form visibility status

function showModal() {
  modalVisible.value = true; // Show modal when button is clicked
}

function closeModal() {
  modalVisible.value = false; // Close modal
  showUsernameForm.value = true; // Show username form again
}

function showFeedbackForm() {
  showUsernameForm.value = false; // Show feedback form
}
</script>

<template>
  <div class="min-h-screen flex justify-center items-center">
    <button class="btn btn-outline" @click="showModal()">Form Pop Up</button>
    <dialog
      id="my_modal_5"
      class="modal modal-bottom sm:modal-middle flex justify-center items-center p-3"
      :open="modalVisible"
    >
      <div class="modal-box">
        <div class="modal-action relative bottom-5 w-full">
          <form method="dialog" class="hover:bg-slate-500 hover:rounded-full">
            <button @click="closeModal()">
              <svg
                class="swap-on fill-current"
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 512 512"
              >
                <polygon
                  points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49"
                />
              </svg>
            </button>
          </form>
        </div>
        <template v-if="showUsernameForm">
          <Username @usernameSubmitted="showFeedbackForm" />
        </template>
        <template v-else>
          <FeedBack @feedbackSubmitted="closeModal" />
        </template>
      </div>
    </dialog>
  </div>
</template>
