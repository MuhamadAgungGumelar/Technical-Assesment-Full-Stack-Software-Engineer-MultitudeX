<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      selectedScore: null,
      message: "", // To display error or success messages
      scores: [1, 2, 3, 4, 5], // Available rating scale
      questions: [
        // List of feedback questions
        "How would you rate your satisfaction with our product?",
        "How useful do you find our features?",
        "How likely are you to recommend our product to others?",
      ],
      currentQuestionIndex: 0, // Current question index
      feedbackData: [], // Holds feedback data to be sent
    };
  },
  methods: {
    async submitFeedback() {
      try {
        if (this.selectedScore === null) {
          // Validation if score is not selected
          this.message = "Please select a score.";
          return;
        } else {
          this.message = ""; // Reset error message
        }

        // Add feedback data to feedbackData array
        this.feedbackData.push({
          question: this.questions[this.currentQuestionIndex],
          score_id: this.selectedScore,
        });

        this.selectedScore = null; // Reset selected score

        if (this.currentQuestionIndex === this.questions.length - 1) {
          // If it's the last question
          const user_id = localStorage.getItem("user_id"); // Get user_id from local storage
          await Promise.all(
            this.feedbackData.map(async (feedback) => {
              await axios.post(
                "http://localhost:8000/feedback/",
                {
                  user_id: user_id,
                  score_id: feedback.score_id,
                  question: feedback.question,
                },
                { withCredentials: true } // Use credentials for authorization
              );
            })
          );

          this.feedbackData = []; // Clear feedbackData array after successful submission
          this.message = "Feedback submitted successfully!";

          // Emit event to close modal after feedback submission
          this.$emit("feedbackSubmitted");

          // Show SweetAlert after successful submission
          Swal.fire({
            title: "Success!",
            text: "Feedback submitted successfully!",
            icon: "success",
            confirmButtonText: "OK",
          }).then(() => {
            // Emit event to close modal and return to main page after SweetAlert is closed
            this.$emit("closeModal");
          });
        } else {
          this.currentQuestionIndex++; // Move to the next question
        }
      } catch (error) {
        console.error("Failed to submit feedback:", error);
        this.message = "Failed to submit feedback.";
      }
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.feedbackData.pop(); // Remove the last feedback data from feedbackData array
        this.currentQuestionIndex--; // Go back to the previous question
        this.selectedScore = null; // Reset selected score
      }
    },
  },
};
</script>

<template>
  <div class="flex flex-col gap-5 justify-center items-center p-10">
    <div v-if="message" role="alert" class="alert alert-warning">
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
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
        />
      </svg>
      <p class="text-slate-100">{{ message }}</p>
    </div>
    <progress
      class="progress progress-success w-full"
      :value="(currentQuestionIndex + 1) * 33.33"
      max="100"
    ></progress>
    <h2 class="text-lg font-bold">
      {{ questions[currentQuestionIndex] }}
    </h2>
    <form
      class="flex flex-col items-center gap-4"
      @submit.prevent="submitFeedback"
    >
      <div class="rating rating-lg flex flex-row gap-7 lg:p-8">
        <label
          class="flex flex-col items-center gap-1"
          v-for="score in scores"
          :key="score"
        >
          <input
            type="radio"
            :name="'rating-' + currentQuestionIndex"
            :value="score"
            v-model="selectedScore"
            @change="selectedScore = score"
            class="mask mask-star-2 bg-slate-500"
            :class="{
              'bg-slate-900': score <= selectedScore,
            }"
          />
          {{ score }}
        </label>
      </div>
      <div class="flex flex-row justify-between w-full text-md font-semibold">
        <p>Very disatisfied</p>
        <p>Very satisfied</p>
      </div>
      <div class="flex justify-end w-full gap-4">
        <button
          v-if="currentQuestionIndex > 0"
          @click.prevent="previousQuestion"
          class="btn btn-outline"
        >
          Previous
        </button>
        <button
          v-if="currentQuestionIndex === questions.length - 1"
          class="btn btn-outline self-end"
          type="submit"
        >
          Submit
        </button>
        <button
          v-else
          class="btn btn-outline self-end"
          type="button"
          @click.prevent="submitFeedback"
        >
          Next
        </button>
      </div>
    </form>
  </div>
</template>
