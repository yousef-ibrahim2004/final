// SocialHub JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeLikeButtons();
    initializeImagePreview();
    initializeFormValidation();
    initializeTooltips();
    initializeInfiniteScroll();
});

// Like button functionality
function initializeLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', handleLike);
    });
}

async function handleLike(event) {
    event.preventDefault();
    
    const button = event.currentTarget;
    const postId = button.dataset.postId;
    const likeCountSpan = button.querySelector('.like-count');
    const heartIcon = button.querySelector('i');
    
    // Disable button during request
    button.disabled = true;
    
    try {
        const response = await fetch(`/post/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Update like count
            likeCountSpan.textContent = data.total_likes;
            
            // Update button state
            if (data.liked) {
                button.classList.add('liked');
                button.classList.remove('btn-outline-primary');
                button.classList.add('btn-primary');
                heartIcon.classList.add('text-danger');
                
                // Add pulse animation
                button.classList.add('pulse');
                setTimeout(() => button.classList.remove('pulse'), 500);
            } else {
                button.classList.remove('liked');
                button.classList.remove('btn-primary');
                button.classList.add('btn-outline-primary');
                heartIcon.classList.remove('text-danger');
            }
        }
    } catch (error) {
        console.error('Error liking post:', error);
        showAlert('Error liking post. Please try again.', 'danger');
    } finally {
        button.disabled = false;
    }
}

// Image preview for file uploads
function initializeImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            const previewId = input.id + '-preview';
            
            // Remove# SocialHub - Django Social Media Platform