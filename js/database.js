import { userID } from "./login.js";

export let userQuestions = [];
export let questionLibrary = [];

let numberOfQuestiosn = 0;

export function addQuestion(newQuestion) {

    fetch('http://127.0.0.1:8001/save_question', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: newQuestion
        })
      })
      .then(response => response.json())
      .then(data => {
          console.log(data);
      })
      .catch(error => {
          console.error('Error:', error);
      });
}
export function addLibraryQuestion(questionID) {
    const question = userQuestions.find(question => String(question.question_id) === String(questionID));
    if (question) {
        questionLibrary.push(question);
    }   
}

export function addUserQuestion(questionID) {
    const question = questionLibrary.find(question => String(question.question_id) === String(questionID));
    if (question) {
        userQuestions.push(question);
    }
}

export function removeUserQuestion(questionID) {
    const index = userQuestions.findIndex(question => String(question.question_id) === String(questionID));
    if (index !== -1) {
        userQuestions.splice(index, 1);
    }
}

export function removeLibraryQuestion(questionID) {
    console.log('question library       :', questionLibrary);
    const index = questionLibrary.findIndex(question => String(question.question_id) === String(questionID));
    console.log("index: ", index, " questionID: ", questionID);
    if (index !== -1) {
        questionLibrary.splice(index, 1);
    }
}

export function save_data() {
fetch('http://127.0.0.1:8001/save_question', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        question: 'What is the capital of France?'
    })
  })
  .then(response => response.json())
  .then(data => {
      console.log(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
  
export async function get_data() {
    try {
      const response = await fetch(`http://127.0.0.1:8001/get_questions?user_id=${userID}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });
      if (!response.ok) {
       return ;
      }
      const data = await response.json();
      questionLibrary = data;
      console.log('General questions:', questionLibrary);
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  }

  export async function get_user_questions() {
    try {
      const response = await fetch(`http://127.0.0.1:8001/get_user_questions?user_id=${userID}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });
      if (!response.ok) {
        return;
      }
      const data = await response.json();
      userQuestions = data;
      console.log('User questions:', userQuestions);
      return data;
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  }