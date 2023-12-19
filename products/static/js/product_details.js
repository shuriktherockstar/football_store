document.addEventListener('DOMContentLoaded', function () {
    const addToCartBtn = document.getElementById('add-to-cart-btn');
    const propertyChoiceSelect = document.querySelector('select[name="property-choice"]');
    const inCartBtn = document.querySelector('.in-cart');

    addToCartBtn.addEventListener('click', function () {
        const productUnitId = propertyChoiceSelect.options[propertyChoiceSelect.selectedIndex].getAttribute('data-product-unit-id');
        const quantity = 1;

        fetch('/add_to_cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                'product_unit_id': productUnitId,
                'quantity': quantity
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addToCartBtn.style.display = 'none';
                    inCartBtn.style.display = 'inline-block';
                } else {
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});