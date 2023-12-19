document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const closeIcon = document.getElementById('close-icon');

    function fadeIn(element) {
        element.style.transition = 'visibility 0s, opacity 0.2 linear';
        element.style.visibility = 'visible';
        element.style.opacity = '1';
    }

    function fadeOut(element) {
        element.style.transition = 'visibility 0s, opacity 0.2s linear';
        element.style.opacity = '0';
        setTimeout(() => {
            element.style.visibility = 'hidden';
        }, 200);
    }

    searchInput.addEventListener('input', function () {
        if (searchInput.value.trim() === '') {
            fadeOut(closeIcon);
        } else {
            fadeIn(closeIcon);
        }
    });

    closeIcon.addEventListener('click', function () {
        searchInput.value = '';
        fadeOut(closeIcon);
    });
});