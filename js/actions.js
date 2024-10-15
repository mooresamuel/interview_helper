import { addUserQuestion, assignQuestion, unassignQuestion, addGeneratedQuestions, load_questions } from "./database.js";
import { updateQuestions, experience, jobTitle } from "./main.js";
import { source } from "./database.js";
import { userID } from "./login.js";

const generateQuestions = document.getElementById('generate-questions');
// const deleteQuestions = document.getElementById('delete-questions');
const transferQuestions = document.getElementById('transfer-questions');
const play = document.getElementById('play');
const userQuestionsWindow = document.getElementById('user-questions-window');
const questionLibraryWindow = document.getElementById('question-library-window');
const generatedQuestionsWindow = document.getElementById('generated-questions-window');
const customQuestion = document.getElementById('custom-question');
const spinner = document.getElementById('spinner-page');

customQuestion.addEventListener('click', () => {

    const question = prompt('Enter your custom question:');
    if (question) {
        addUserQuestion(question);
    }
});

generateQuestions.addEventListener('click', async () => {
    spinner.classList.remove('hidden');
    spinner.style.display = 'flex';
    fetch(`${source}generate_questions`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userID,
            job_title: jobTitle,
            experience: experience
        })
    })
    .then(response => {
        console.log('Response:', response);
        return response.json();
    })
    .then(data => {
        let result = [];
        data.forEach(item => {
            if (Array.isArray(item) && item.length > 0) {
                const question = item[0].question_text; // Extract the question object
                console.log("question result array: ", question);
                result.push({question_text: question, question_id: item[0].question_id});
            }
        });
        addGeneratedQuestions(result);
    })
    .then(() => {
        updateQuestions();
        spinner.classList.add('hidden');
        spinner.style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});



transferQuestions.addEventListener('click', () => {
    const libraryButtons = questionLibraryWindow.querySelectorAll('.btn-check');
    let matched = 0;
    libraryButtons.forEach(button => {
        if (button.checked) {
            assignQuestion(button.id);
            matched++;
        }
    });
    const generatedButtons = generatedQuestionsWindow.querySelectorAll('.btn-check');
    generatedButtons.forEach(button => {
        if (button.checked) {
            assignQuestion(button.id, 'generated');
            matched++;
        }
    });
    const userButtons = userQuestionsWindow.querySelectorAll('.btn-check');
    userButtons.forEach(button => {
        if (button.checked) {
            unassignQuestion(button.id);
            matched++;
        }
    });
    if (matched === 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No questions selected, choose some questions to move!',
        });
    } else {
        load_questions();
        updateQuestions();
    }
});
