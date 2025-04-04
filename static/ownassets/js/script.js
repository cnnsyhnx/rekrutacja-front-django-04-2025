// Custom JavaScript for Event Manager

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle form validation messages
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                // Focus the first invalid field for accessibility
                const invalidField = form.querySelector(':invalid');
                if (invalidField) {
                    invalidField.focus();
                }
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Monthly calendar event handling
    const calendarEvents = document.querySelectorAll('.calendar-event');
    if (calendarEvents.length > 0) {
        calendarEvents.forEach(event => {
            event.addEventListener('click', function(e) {
                e.preventDefault();
                const eventId = this.getAttribute('data-event-id');
                if (eventId) {
                    window.location.href = `/events/${eventId}/`;
                }
            });

            // Make calendar accessible via keyboard
            event.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        });
    }

    // Handle confirmation dialogs
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    if (confirmButtons.length > 0) {
        confirmButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const message = this.getAttribute('data-confirm');
                const href = this.getAttribute('href');
                
                Swal.fire({
                    title: 'Are you sure?',
                    text: message || "You won't be able to revert this!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#003d7c',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes, proceed!',
                    cancelButtonText: 'Cancel'
                }).then((result) => {
                    if (result.isConfirmed && href) {
                        window.location.href = href;
                    }
                });
            });
        });
    }

    // Accessibility features
    // Add role attributes to dynamic elements
    const eventCards = document.querySelectorAll('.event-card');
    if (eventCards.length > 0) {
        eventCards.forEach(card => {
            card.setAttribute('role', 'article');
        });
    }
    
    // Ensure all buttons have accessible names
    const buttons = document.querySelectorAll('button:not([aria-label]):not([title])');
    if (buttons.length > 0) {
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                const prevEl = button.previousElementSibling;
                if (prevEl && prevEl.textContent) {
                    button.setAttribute('aria-label', prevEl.textContent.trim());
                }
            }
        });
    }
});

// Initialize monthly calendar if it exists
function initializeMonthlyCalendar() {
    const calendarContainer = document.getElementById('calendar-container');
    if (!calendarContainer) return;

    // Handle month navigation
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const currentMonthBtn = document.getElementById('current-month');

    if (prevMonthBtn) {
        prevMonthBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            if (url) window.location.href = url;
        });
    }

    if (nextMonthBtn) {
        nextMonthBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            if (url) window.location.href = url;
        });
    }

    if (currentMonthBtn) {
        currentMonthBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            if (url) window.location.href = url;
        });
    }
}

// Call the calendar initialization function when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeMonthlyCalendar);
