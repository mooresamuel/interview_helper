import { userID } from "./login.js";
import { updateQuestions } from "./main.js";

export let userQuestions = [];
export let questionLibrary = [];


// export const source = 'https://samalmoore1.eu.pythonanywhere.export com/';
export const source = 'http://127.0.0.1:8001/'

export function addUserQuestion(newQuestion) {  ///user master password 1 to add questions
  console.log("userID: ", userID);
  fetch(`${source}/add_user_question`, {
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
        console.log("data  ",data);
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

export function moveIntoUserQuestions(id) {  ///user master password 1 to add questions
  console.log("userID: ", userID);
  fetch(`${source}/move_into_user_questions`, {
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
    .then(response => response.json())
    .then(data => {
        console.log(data);
        userQuestions.push(questionLibrary.find(question => String(question.question_id) === String(id)));
        questionLibrary = questionLibrary.filter(question => String(question.question_id) !== String(id));
          updateQuestions();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

export function moveOutOfUserQuestions(id) {
  console.log("userID: ", userID);
  fetch(`${source}/move_out_of_user_questions`, {
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
    .then(response => response.json())
    .then(data => {
        console.log(data);
        questionLibrary.push(userQuestions.find(question => String(question.question_id) === String(id)));
        userQuestions = userQuestions.filter(question => String(question.question_id) !== String(id));
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
fetch(`${source}/save_question`, {
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
      const response = await fetch(`${source}/get_questions?user_id=${userID}`, {
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
      const response = await fetch(`${source}/get_user_questions?user_id=${userID}`, {
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