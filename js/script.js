import { get_data, get_user_questions } from './database.js';
import { userID } from './login.js';

const questions = document.querySelector('.questions');

// Function to fetch and display data
async function fetchAndDisplayData() {
  try {
    const data = await get_data(); // Ensure get_data returns a promise
    console.log(data);
    data.forEach(element => {
      questions.innerHTML += `<div class="question-text" id="${element.question_id}">${element.question_text}</div>`;
    });
  } catch (error) {
    console.error('Error fetching data:', error);
  }

}

// Call the function to fetch and display data
fetchAndDisplayData();

