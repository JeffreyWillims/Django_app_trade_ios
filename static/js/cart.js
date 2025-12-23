/**
 * ====================================================================
 * iOStrade - Cart Interaction Logic (AJAX)
 * Version: 2.0 (Full Functionality)
 * ====================================================================
 */

/**
 * Получает CSRF-токен из cookie.
 * @param {string} name - Имя cookie (обычно 'csrftoken').
 * @returns {string|null} - Значение токена или null.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Начинается ли строка с имени, которое мы ищем?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/**
 * Обновляет все компоненты корзины и счетчики на странице.
 * @param {object} data - JSON-объект, полученный от сервера.
 */
function updateUI(data) {
    // Обновляем основной компонент корзины (в модальном окне, на странице профиля)
    const cartContainers = document.querySelectorAll('.cart-component-container');
    if (cartContainers.length > 0 && data.cart_component_html) {
        cartContainers.forEach(container => {
            container.innerHTML = data.cart_component_html;
        });
    }

    // Обновляем все счетчики
    const counterBadges = document.querySelectorAll('.cart-counter-badge');
    if (counterBadges.length > 0 && typeof data.total_quantity !== 'undefined') {
        counterBadges.forEach(badge => {
            badge.textContent = data.total_quantity;
            badge.style.display = data.total_quantity > 0 ? 'inline-block' : 'none';
        });
    }
}


// Основной "прослушиватель" событий, который срабатывает при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {

    // Используем делегирование событий: один "слушатель" на весь body
    document.body.addEventListener('click', async (event) => {

        // Ищем, был ли клик по кнопке добавления или удаления
        const simpleCartButton = event.target.closest('.add-to-cart-btn, .remove-from-cart-btn');
        // Ищем, был ли клик по кнопке изменения количества
        const quantityChangeButton = event.target.closest('.cart-quantity-change');

        // --- Обработчик для ДОБАВЛЕНИЯ / УДАЛЕНИЯ (GET-запрос) ---
        if (simpleCartButton) {
            event.preventDefault(); // Отменяем стандартный переход по ссылке
            const url = simpleCartButton.href;

            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                });
                if (!response.ok) throw new Error('Network error on GET request.');

                const data = await response.json();
                updateUI(data); // Обновляем интерфейс
            } catch (error) {
                console.error('AJAX GET Error:', error);
                window.location.reload(); // Запасной вариант: перезагрузить страницу
            }
        }

        // --- Обработчик для ИЗМЕНЕНИЯ КОЛИЧЕСТВА (POST-запрос) ---
        if (quantityChangeButton) {
            event.preventDefault();
            const url = quantityChangeButton.dataset.url;
            const action = quantityChangeButton.dataset.action;
            const csrfToken = getCookie('csrftoken'); // Получаем CSRF-токен

            const formData = new FormData();
            formData.append('action', action);

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken, // Отправляем CSRF-токен в заголовке
                    },
                    body: formData,
                });
                if (!response.ok) throw new Error('Network error on POST request.');

                const data = await response.json();
                updateUI(data); // Обновляем интерфейс
            } catch (error) {
                console.error('AJAX POST Error:', error);
                window.location.reload(); // Запасной вариант
            }
        }
    });
});