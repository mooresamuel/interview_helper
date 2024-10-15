import { userID } from "./login.js";
import { updateQuestions } from "./main.js";

export let userQuestions = [];
export let questionLibrary = [];
export let generatedQuestions = [];


export const source = 'https://samalmoore1.eu.pythonanywhere.com/';
// export const source = 'http://127.0.0.1:8001/'


export async function addGeneratedQuestions(questions) {
    questions.forEach(question => {
        generatedQuestions.push(question);
    });
}

export function addUserQuestion(newQuestion) {  
  let is_common = false;
  let is_generated = false;
  console.log("userID: ", userID);
  if (userID === 1) {
    is_common = true;
  }
  fetch(`${source}save_question`, {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          question_text: newQuestion,
          user_id: userID,
          is_generated: is_generated,
          is_common: is_common,
          is_saved: true
      })
    })
    .then(response => response.json())
    .then(data => {
        userQuestions.push({          
          question_text: newQuestion,
          question_id: data.question_id,
          user_id: userID});
    })
    .then(() => {
        updateQuestions();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

export function assignQuestion(id, type) {
  fetch(`${source}assign_question`, {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          question_id: id,
          user_id: userID
      })
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


export function unassignQuestion(id) {
  fetch(`${source}unassign_question`, {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          question_id: id,
          user_id: userID
      })
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
  
export async function load_questions() {
  try {
    const response = await fetch(`${source}load_questions?user_id=${userID}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });
    if (!response.ok) {
     return ;
    }
    const data = await response.json();
    data.forEach(question => {
      if (question.is_saved) {
        userQuestions.push(question);
      } else if (question.common) {
        questionLibrary.push(question);
      } else if (question.generated) {
        generatedQuestions.push(question);
      }
    });
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}