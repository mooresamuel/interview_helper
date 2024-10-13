import { userID } from "./login.js";
import { updateQuestions } from "./main.js";

export let userQuestions = [];
export let questionLibrary = [];

let numberOfQuestiosn = 0;

export function addQuestion(newQuestion) {

    fetch('https://samalmoore1.eu.pythonanywhere.com/save_question', {
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

export function addUserQuestion(newQuestion) {

  fetch('https://samalmoore1.eu.pythonanywhere.com/add_user_question', {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          question: newQuestion,
          user_id: userID
      })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        userQuestions.push({          
          question: newQuestion,
          user_id: userID});
          updateQuestions();
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
fetch('https://samalmoore1.eu.pythonanywhere.com/save_question', {
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
      const response = await fetch(`https://samalmoore1.eu.pythonanywhere.com/get_questions?user_id=${userID}`, {
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
      const response = await fetch(`https://samalmoore1.eu.pythonanywhere.com/get_user_questions?user_id=${userID}`, {
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