import { addUserQuestion, removeLibraryQuestion, addQuestion, addLibraryQuestion, removeUserQuestion } from "./database.js";
import { updateQuestions } from "./main.js";

const generateQuestions = document.getElementById('generate-questions');
const deleteQuestions = document.getElementById('delete-questions');
const importQuestions = document.getElementById('import-questions');
const play = document.getElementById('play');
const userQuestionsWindow = document.getElementById('user-questions-window');
const questionLibraryWindow = document.getElementById('question-library-window');
const customQuestion = document.getElementById('custom-question');

console.log("actions.js");  

customQuestion.addEventListener('click', () => {
    const question = prompt('Enter your custom question:');
    if (question) {
        addUserQuestion(question);
    }
});

// deleteQuestions.addEventListener('click', () => {
//     const buttons = userQuestionsWindow.querySelectorAll('.btn-check');
//     let matched = 0;
//     buttons.forEach(button => {
//         if (button.checked) {
//             addLibraryQuestion(button.id);
//             removeUserQuestion(button.id);
//             updateQuestions();
//             matched++;
//         }
//     });
//     if (matched === 0) {
//         Swal.fire({
//             icon: 'error',
//             title: 'Error',
//             text: 'No questions selected, choose some questions to delete!',
//         });
//     }
// });

// importQuestions.addEventListener('click', () => {
//     const buttons = questionLibraryWindow.querySelectorAll('.btn-check');
//     let matched = 0;
//     console.log("clcik: ");
//     buttons.forEach(button => {
//         if (button.checked) {
//             console.log(button);
//             addUserQuestion(button.id);
//             removeLibraryQuestion(button.id);
//             updateQuestions();
//             matched++;
//         }
//     });
//     if (matched === 0) {
//         Swal.fire({
//             icon: 'error',
//             title: 'Error',
//             text: 'No questions selected, choose some questions to import!',
//         });
//     }
// });
