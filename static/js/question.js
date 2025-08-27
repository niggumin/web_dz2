document.addEventListener('DOMContentLoaded', function() {
    function handleVote(event) {
        event.preventDefault();
        const button = event.currentTarget;
        const id = button.dataset.id;
        const action = button.dataset.action;
        const type = button.dataset.type;
        const url = `/${type}/${id}/${action}/`;
        const csrftoken = getCookie('csrftoken');
        
        

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
            mode: 'same-origin'
        })
        .then(response => {
            if (response.status === 404) {
                // const nextUrl = encodeURIComponent(window.location.pathname);
                window.location.href = '/login';
                alert("You need to log in before voting")
                return;
            }
            return response.json();
        })
        .then(data => {
            const likeCountElement = button.querySelector('.like-count');
            const dislikeCountElement = button.querySelector('.dislike-count');
            
            if (action === 'like') {
                if (likeCountElement) likeCountElement.textContent = data.likes_count;
                const dislikeBtn = button.closest('.btn-group-vertical').querySelector('.dislike-btn');
                if (dislikeBtn) {
                    dislikeBtn.classList.remove('active');
                    if (dislikeBtn.querySelector('.dislike-count')) {
                        dislikeBtn.querySelector('.dislike-count').textContent = data.dislikes_count;
                    }
                }
                button.classList.toggle('active');
            } else {
                if (dislikeCountElement) dislikeCountElement.textContent = data.dislikes_count;
                const likeBtn = button.closest('.btn-group-vertical').querySelector('.like-btn');
                if (likeBtn) {
                    likeBtn.classList.remove('active');
                    if (likeBtn.querySelector('.like-count')) {
                        likeBtn.querySelector('.like-count').textContent = data.likes_count;
                    }
                }
                button.classList.toggle('active');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    document.querySelectorAll('.like-btn, .dislike-btn').forEach(button => {
        button.addEventListener('click', handleVote);
    });
});