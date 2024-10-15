import { userID } from "./login.js";
import { updateQuestions } from "./main.js";

export let userQuestions = [];
export let questionLibrary = [];
export let generatedQuestions = [];


// export const source = 'https://samalmoore1.eu.pythonanywhere.export com/';
export const source = 'http://127.0.0.1:8001/'

export function addUserQuestion(newQuestion) {  ///user master password 1 to add questions
  console.log("userID: ", userID);
  let is_common = false;
  let is_generated = false;
  console.log("userID: ", userID);
  if (userID === 2) {
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

export function assignQuestion(id, type) {  ///user master password 1 to add questions
  console.log("userID: ", userID);
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
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (type === 'generated') {
          userQuestions.push(generatedQuestions.find(question => String(question.question_id) === String(id)));
          generatedQuestions = generatedQuestions.filter(question => String(question.question_id) !== String(id));
        } else {
          userQuestions.push(questionLibrary.find(question => String(question.question_id) === String(id)));
          questionLibrary = questionLibrary.filter(question => String(question.question_id) !== String(id));
        }
        updateQuestions();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

export function unassignQuestion(id) {
  console.log("userID: ", userID);
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
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // questionLibrary.push(userQuestions.find(question => String(question.question_id) === String(id)));
        // userQuestions = userQuestions.filter(question => String(question.question_id) !== String(id));
        //   updateQuestions();
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
fetch(`${source}save_question`, {
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
    // ~userquestions questionLibrary generatedQuestions
    const data = await response.json();
    data.forEach(question => {
      console.log("question: ", question);
      if (question.is_saved) {
        userQuestions.push(question);
      } else if (question.common) {
        questionLibrary.push(question);
      } else if (question.generated) {
        generatedQuestions.push(question);
      }
    });

    console.log('General questions:', questionLibrary);
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}
// export async function get_data() {
//     try {
//       const response = await fetch(`${source}get_questions?user_id=${userID}`, {
//         method: 'GET',
//         headers: {
//           'Accept': 'application/json'
//         }
//       });
//       if (!response.ok) {
//        return ;
//       }
//       const data = await response.json();
//       questionLibrary = data;
//       console.log('General questions:', questionLibrary);
//     } catch (error) {
//       console.error('Error fetching data:', error);
//       throw error;
//     }
//   }

//   export async function get_user_questions() {
//     try {
//       const response = await fetch(`${source}get_user_questions?user_id=${userID}`, {
//         method: 'GET',
//         headers: {
//           'Accept': 'application/json'
//         }
//       });
//       if (!response.ok) {
//         return;
//       }
//       const data = await response.json();
//       userQuestions = data;
//       console.log('User questions:', userQuestions);
//       return data;
//     } catch (error) {
//       console.error('Error fetching data:', error);
//       throw error;
//     }
//   }

//   export async function get_generated_questions() {
//     try {
//       const response = await fetch(`${source}get_generated_questions?user_id=${userID}`, {
//         method: 'GET',
//         headers: {
//           'Accept': 'application/json'
//         }
//       });
//       if (!response.ok) {
//         return;
//       }
//       const data = await response.json();
//       generatedQuestions = data;
//       console.log('User questions:', generatedQuestions);
//       return data;
//     } catch (error) {
//       console.error('Error fetching data:', error);
//       throw error;
//     }
//   }