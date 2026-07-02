// index.js — homepage news-card video previews.
// Site-wide behavior (nav animations, sidebar, message toasts, .btn hover) is
// handled by base.js; this file only covers what's unique to the homepage.

document.addEventListener('DOMContentLoaded', function () {
    const videos = document.querySelectorAll('.news-video');

    videos.forEach(video => {
        // Muted is required for autoplay in every modern browser
        video.muted = true;
        video.volume = 0;

        const playPromise = video.play();

        if (playPromise !== undefined) {
            playPromise.catch(() => {
                // Autoplay was blocked — retry on the first user interaction
                document.addEventListener('click', function playOnClick() {
                    video.play();
                    document.removeEventListener('click', playOnClick);
                }, { once: true });
            });
        }

        // Pause the video and let the overlay show while hovering the card
        const card = video.closest('.news-card');
        if (card) {
            card.addEventListener('mouseenter', () => video.pause());
            card.addEventListener('mouseleave', () => video.play());
        }
    });
});