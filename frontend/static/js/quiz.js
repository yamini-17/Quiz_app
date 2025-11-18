// quiz.js - Quiz functionality

async function loadQuizzes() {
    try {
        const response = await fetch('/quizzes');  // FIXED
        const data = await response.json();

        const container = document.getElementById('quizzesContainer');
        container.innerHTML = '';

        if (!data.quizzes || data.quizzes.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: grey; grid-column: 1 / -1;">No quizzes available yet.</p>';
            return;
        }

        data.quizzes.forEach(quiz => {
            const quizCard = document.createElement('div');
            quizCard.className = 'quiz-card';

            quizCard.innerHTML = `
                <h3 class="quiz-title">${quiz.title}</h3>
                <p class="quiz-description">${quiz.description}</p>
                <button class="btn btn-primary" onclick="startQuiz(${quiz.id})">Start Quiz</button>
            `;

            container.appendChild(quizCard);
        });
    } catch (error) {
        console.error('Error loading quizzes:', error);
        document.getElementById('quizzesContainer').innerHTML =
            '<p style="text-align: center; color: red;">Error loading quizzes</p>';
    }
}

function startQuiz(id) {
    window.location.href = `/quiz/${id}`;
}
