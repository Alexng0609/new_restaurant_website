// Initialize GSAP
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', function () {
    // Animate navigation
    gsap.from('nav', {
        y: -100,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    });

    // Animate cards on scroll
    gsap.utils.toArray('.card').forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            duration: 0.8,
            delay: index * 0.1,
            ease: 'power2.out'
        });
    });

    // Animate fade-in elements
    document.querySelectorAll('.fade-in').forEach(el => {
        el.classList.add('active');
    });

    // Smooth scroll for anchor links
    // (native scrollIntoView — no ScrollToPlugin required)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // News card videos: autoplay muted, pause on hover so the overlay shows.
    // Shared by any page using the .news-card component (homepage, feeds, ...).
    document.querySelectorAll('.news-card-media video').forEach(video => {
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

        const card = video.closest('.news-card');
        if (card) {
            card.addEventListener('mouseenter', () => video.pause());
            card.addEventListener('mouseleave', () => video.play());
        }
    });

    // Admin edit/delete controls layered on a clickable card shouldn't
    // trigger the card's own link underneath them.
    document.querySelectorAll('.admin-controls a, .admin-controls button').forEach(control => {
        control.addEventListener('click', e => e.stopPropagation());
    });

    // Hover animations for buttons
    document.querySelectorAll('.view-reviews-btn').forEach(btn => {
        btn.addEventListener('mouseenter', function () {
            gsap.to(this, {
                scale: 1.05,
                duration: 0.3,
                ease: 'power2.out'
            });
        });

        btn.addEventListener('mouseleave', function () {
            gsap.to(this, {
                scale: 1,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });

    // Sidebar menu: opens/closes the panel holding every site page
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sideMenuClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const sideMenu = document.getElementById('sideMenu');

    if (sidebarToggle && sideMenu && sidebarOverlay) {
        const openSidebar = function () {
            sideMenu.classList.add('active');
            sidebarOverlay.classList.add('active');
            document.body.classList.add('sidebar-open');
            sidebarToggle.setAttribute('aria-expanded', 'true');
            sideMenu.setAttribute('aria-hidden', 'false');
        };

        const closeSidebar = function () {
            sideMenu.classList.remove('active');
            sidebarOverlay.classList.remove('active');
            document.body.classList.remove('sidebar-open');
            sidebarToggle.setAttribute('aria-expanded', 'false');
            sideMenu.setAttribute('aria-hidden', 'true');
        };

        sidebarToggle.addEventListener('click', function () {
            sideMenu.classList.contains('active') ? closeSidebar() : openSidebar();
        });

        if (sidebarClose) {
            sidebarClose.addEventListener('click', closeSidebar);
        }

        sidebarOverlay.addEventListener('click', closeSidebar);

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeSidebar();
        });
    }

    // Add-to-cart forms (menu page): AJAX submit + toast feedback.
    // Only present on pages that render .add-to-cart-form, so this is a
    // no-op everywhere else.
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const button = this.querySelector('.add-btn');
            const originalText = button.textContent;
            const itemName = this.dataset.itemName;

            button.disabled = true;
            button.textContent = 'Đang thêm...';

            const formData = new FormData(this);

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update both cart badges (nav icon + sidebar link),
                    // creating them if the cart was empty on page load
                    // (Django doesn't render the <span> at all when count is 0).
                    updateCartBadge('cart-count', data.cart_total_items, '.cart-link');
                    updateCartBadge('cart-count-sidebar', data.cart_total_items, '.sidebar-cart-link');

                    showToast(`✓ Đã thêm "${itemName}" vào giỏ hàng!`, 'success');

                    button.disabled = false;
                    button.textContent = originalText;
                } else {
                    showToast(data.error || 'Lỗi khi thêm vào giỏ hàng', 'error');
                    button.disabled = false;
                    button.textContent = originalText;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Lỗi kết nối mạng', 'error');
                button.disabled = false;
                button.textContent = originalText;
            });
        });
    });

    // Updates a cart badge <span> by id, creating it inside the given
    // container if it doesn't exist yet (happens on the very first add
    // to cart, since Django only renders the badge when cart_count > 0).
    function updateCartBadge(id, count, containerSelector) {
        let badge = document.getElementById(id);
        if (badge) {
            badge.textContent = count;
            return;
        }
        const container = document.querySelector(containerSelector);
        if (!container) return;

        badge = document.createElement('span');
        badge.className = 'cart-badge';
        badge.id = id;
        badge.textContent = count;
        container.appendChild(badge);
    }

    // Toast notification helper — used by the add-to-cart handler above.
    // Guarded on #toast-container so it's harmless on pages without one.
    function showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.style.background = type === 'success' ? '#28a745' : '#dc3545';
        toast.innerHTML = `
            <span style="font-size: 1.5rem;">${type === 'success' ? '✓' : '✗'}</span>
            <span>${message}</span>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('hide');
            setTimeout(() => {
                container.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // Messages: close button + slide-in + 15s auto-dismiss
    document.querySelectorAll('.message').forEach(message => {
        const closeBtn = document.createElement('button');
        closeBtn.className = 'close-message';
        closeBtn.innerHTML = '<i class="fas fa-times"></i>';
        closeBtn.onclick = function () {
            message.style.transition = 'all 0.3s ease';
            message.style.opacity = '0';
            message.style.transform = 'translateX(-50px)';
            setTimeout(() => message.remove(), 300);
        };
        message.appendChild(closeBtn);

        message.style.opacity = '0';
        message.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            message.style.transition = 'all 0.5s ease';
            message.style.opacity = '1';
            message.style.transform = 'translateX(0)';
        }, 100);

        setTimeout(() => {
            message.style.transition = 'all 0.5s ease';
            message.style.opacity = '0';
            message.style.transform = 'translateX(-50px)';
            setTimeout(() => message.remove(), 500);
        }, 15000); // 15 seconds
    });
});