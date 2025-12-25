document.addEventListener('DOMContentLoaded', function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function showToast(message, status = 'success') {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) return;
        const toastColor = status === 'success' ? 'primary' : 'danger';
        const toastId = `toast-${Date.now()}`;
        const toastHTML = `<div id="${toastId}" class="toast align-items-center text-bg-${toastColor} border-0" role="alert" aria-live="assertive" aria-atomic="true"><div class="d-flex"><div class="toast-body">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div></div>`;
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        const newToastEl = document.getElementById(toastId);
        const newToast = new bootstrap.Toast(newToastEl, { delay: 3000 });
        newToast.show();
        newToastEl.addEventListener('hidden.bs.toast', () => newToastEl.remove());
    }
    function updateUI(data) {
        if (data.cart_component_html) {
            document.querySelectorAll('.cart-component-container').forEach(c => { c.innerHTML = data.cart_component_html; });
        }
        if (typeof data.total_quantity !== 'undefined') {
            document.querySelectorAll('.cart-counter-badge').forEach(b => {
                b.textContent = data.total_quantity;
                b.style.display = data.total_quantity > 0 ? 'inline-block' : 'none';
            });
        }
    }
    document.body.addEventListener('click', async (event) => {
        const button = event.target.closest('.ajax-cart-btn');
        if (!button) return;
        event.preventDefault();
        const url = button.dataset.url || button.href;
        const method = button.dataset.method || 'GET';
        let headers = { 'X-Requested-With': 'XMLHttpRequest' };
        let body = null;
        if (method === 'POST') {
            const csrfToken = getCookie('csrftoken');
            if (!csrfToken) {
                console.error('CSRF token not found!');
                showToast('Ошибка безопасности.', 'error');
                return;
            }
            headers['X-CSRFToken'] = csrfToken;
            const formData = new FormData();
            if (button.dataset.action) {
                formData.append('action', button.dataset.action);
            }
            body = formData;
        }
        try {
            const response = await fetch(url, { method, headers, body });
            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            const data = await response.json();
            updateUI(data);
            if (data.message) {
                showToast(data.message);
            }
        } catch (error) {
            console.error('AJAX Error:', error);
            showToast('Ошибка. Обновите страницу.', 'error');
        }
    });
});