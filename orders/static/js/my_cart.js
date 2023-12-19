document.addEventListener('DOMContentLoaded', function () {
    const decrementButtons = document.querySelectorAll('.decrement-button');
    const incrementButtons = document.querySelectorAll('.increment-button');
    const quantityValues = document.querySelectorAll('.quantity-value');

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    $.ajaxSetup({
        headers: {'X-CSRFToken': csrfToken}
    });

    for (let i = 0; i < decrementButtons.length; i++) {
        const decrementButton = decrementButtons[i];
        const incrementButton = incrementButtons[i];
        const quantityValue = quantityValues[i];

        const cartItemQuantity = parseInt(quantityValue.innerText);
        const productQuantity = parseInt(quantityValue.dataset.productQuantity);

        if (cartItemQuantity === 1) {
            decrementButton.disabled = true;
        }
        if (cartItemQuantity === productQuantity) {
            incrementButton.disabled = true;
        }

        decrementButton.addEventListener('mouseenter', handleMouseEnter);
        incrementButton.addEventListener('mouseenter', handleMouseEnter);

        decrementButton.addEventListener('click', handleDecrement);
        incrementButton.addEventListener('click', handleIncrement);
    }

    function handleMouseEnter(event) {
        const button = event.target;

        if (!button.disabled) {
            button.style.cursor = 'pointer';
        }
    }

    function handleDecrement() {
        const quantityValue = this.nextElementSibling.querySelector('b');
        let currentValue = parseInt(quantityValue.innerText);
        const cartItemId = quantityValue.parentElement.dataset.cartItemId;

        if (currentValue > 1) {
            currentValue--;
            quantityValue.innerText = currentValue;
            updateQuantity(quantityValue, currentValue, cartItemId);
        }

        updateStyles(quantityValue, currentValue);
    }

    function handleIncrement() {
        const quantityValue = this.parentElement.querySelector('.quantity-value .quantity-number');
        let currentValue = parseInt(quantityValue.innerText);
        const productQuantity = parseInt(quantityValue.parentElement.dataset.productQuantity);
        const cartItemId = quantityValue.parentElement.dataset.cartItemId;

        if (currentValue !== productQuantity) {
            currentValue++;
            quantityValue.innerText = currentValue;
            updateQuantity(quantityValue, currentValue, cartItemId);
        }

        updateStyles(quantityValue, currentValue);
    }

    function updateQuantity(quantityElement, newValue, cartItemId) {
        $.ajax({
            url: '/update_quantity/', method: 'POST', data: {
                new_quantity: newValue, cart_item_id: cartItemId,
            }, success: function (response) {
                quantityElement.innerText = newValue;
                const totalPriceElement = document.querySelector('.total-price');
                if (totalPriceElement) {
                    totalPriceElement.innerText = response.total_price;
                }
            }, error: function (error) {
                console.error('Error updating quantity:', error);
            }
        });
    }
});

const deleteButtons = document.querySelectorAll('.delete-button');

deleteButtons.forEach(button => {
    button.addEventListener('click', handleDelete);
});

function handleDelete(event) {
    event.preventDefault();

    const cartItemElement = this.closest('.cart-item');
    if (cartItemElement) {
        const cartItemId = this.dataset.cartItemId;

        $.ajax({
            url: '/delete_cart_item/', method: 'POST', data: {
                cart_item_id: cartItemId,
            }, success: function () {
                cartItemElement.remove();

                const remainingCartItems = document.querySelectorAll('.cart-item');
                if (remainingCartItems.length === 0) {
                    location.reload();
                }
            }, error: function (error) {
                console.error('Error deleting cart item:', error);
            }
        });
    }
}

function updateStyles(quantityValue, currentValue) {
    const decrementButton = quantityValue.parentElement.previousElementSibling;
    const incrementButton = quantityValue.parentElement.nextElementSibling;

    decrementButton.disabled = currentValue === 1;
    incrementButton.disabled = currentValue === parseInt(quantityValue.parentElement.dataset.productQuantity);
}