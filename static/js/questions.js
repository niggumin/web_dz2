document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');
    const dislikeButtons = document.querySelectorAll('.dislike-btn');


    function handleVote(event) {
        const button = event.target;
        const questionId = button.dataset.questionId;
        const action = button.dataset.action;
        const url = `/question/${questionId}/${action}/`;
        const csrftoken = getCookie('csrftoken');

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            mode: 'same-origin'
        })
        .then(response => {
            if (response.status === 404) {
                window.location.href = 'login';
                alert("You need to log in before voting")
                return;
            }
            return response.json();
        })
        .then(data => {
            const questionCard = button.closest('.card');
            questionCard.querySelector('.like-count').textContent = data.likes_count;
            questionCard.querySelector('.dislike-count').textContent = data.dislikes_count;
            
            
            if (action === 'like') {
                button.classList.toggle('active');
                questionCard.querySelector('.dislike-btn').classList.remove('active');
            } else {
                button.classList.toggle('active');
                questionCard.querySelector('.like-btn').classList.remove('active');
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    likeButtons.forEach(button => {
        button.addEventListener('click', handleVote);
    });
    
    dislikeButtons.forEach(button => {
        button.addEventListener('click', handleVote);
    });
});