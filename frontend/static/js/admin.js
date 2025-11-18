// admin.js - Admin functionality

async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();
        
        const select = document.getElementById('quizCategory');
        if (select) {
            select.innerHTML = '<option value="">Select a category</option>';
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function createCategory() {
    const name = document.getElementById('categoryName').value;
    const description = document.getElementById('categoryDescription').value;
    
    try {
        const response = await fetch('/api/admin/categories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Category created successfully!');
            document.getElementById('categoryModal').style.display = 'none';
            document.getElementById('categoryForm').reset();
            loadCategories();
            loadAdminStats();
        } else {
            alert(data.message || 'Error creating category');
        }
    } catch (error) {
        alert('An error occurred');
    }
}

async function loadAdminStats() {
    try {
        // Load quizzes
        const quizzesResponse = await fetch('/api/quizzes');
        const quizzesData = await quizzesResponse.json();
        
        // Load categories
        const categoriesResponse = await fetch('/api/categories');
        const categoriesData = await categoriesResponse.json();
        
        // Update stats
        if (document.getElementById('totalQuizzes')) {
            document.getElementById('totalQuizzes').textContent = quizzesData.quizzes.length;
        }
        
        if (document.getElementById('totalCategories')) {
            document.getElementById('totalCategories').textContent = categoriesData.categories.length;
        }
        
        // Count total questions
        let totalQuestions = 0;
        for (const quiz of quizzesData.quizzes) {
            const questionsResponse = await fetch(`/api/admin/quizzes/${quiz.id}/questions`);
            const questionsData = await questionsResponse.json();
            totalQuestions += questionsData.questions.length;
        }
        
        if (document.getElementById('totalQuestions')) {
            document.getElementById('totalQuestions').textContent = totalQuestions;
        }
        
        // Display recent quizzes
        displayRecentQuizzes(quizzesData.quizzes.slice(0, 5));
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayRecentQuizzes(quizzes) {
    const container = document.getElementById('recentQuizzes');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (quizzes.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No quizzes yet</p>';
        return;
    }
    
    const table = document.createElement('table');
    table.className = 'leaderboard-table';
    table.innerHTML = `
        <thead>
            <tr>
                <th>Title</th>
                <th>Category</th>
                <th>Time Limit</th>
                <th>Created By</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="recentQuizzesBody"></tbody>
    `;
    
    const tbody = table.querySelector('#recentQuizzesBody');
    
    quizzes.forEach(quiz => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${quiz.title}</strong></td>
            <td>${quiz.category_name || 'Uncategorized'}</td>
            <td>${quiz.time_limit} min</td>
            <td>${quiz.created_by_name}</td>
            <td>
                <a href="/admin/questions/${quiz.id}" class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.875rem;">Manage</a>
            </td>
        `;
        tbody.appendChild(row);
    });
    
    container.appendChild(table);
}