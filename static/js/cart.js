document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('click', async (event) => {
        const cartButton = event.target.closest('.add-to-cart-btn, .remove-from-cart-btn');
        if (cartButton) {
            event.preventDefault();
            const url = cartButton.href;
            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                });
                if (!response.ok) throw new Error('Network error');
                const data = await response.json();

                // Обновляем компонент корзины (в модальном окне и профиле)
                document.querySelectorAll('.cart-component-container').forEach(container => {
                    container.innerHTML = data.cart_component_html;
                });

                // Обновляем ВСЕ счетчики на странице
                document.querySelectorAll('.cart-counter-badge').forEach(badge => {
                    badge.textContent = data.total_quantity;
                    if (data.total_quantity > 0) {
                        badge.style.display = 'inline-block';
                    } else {
                        badge.style.display = 'none';
                    }
                });

            } catch (error) {
                console.error('AJAX Error:', error);
                window.location.reload();
            }
        }
    });
});