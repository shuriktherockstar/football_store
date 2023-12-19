$(document).ready(function () {
    $('.delete-button').click(function () {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        $.ajaxSetup({
            headers: {'X-CSRFToken': csrfToken}
        });
        let addressId = $(this).data('address-id');
        $.ajax({
            url: '/delete_address/',
            type: 'POST',
            data: {address_id: addressId},
            dataType: "json",
            success: function (data) {
                location.reload()
            },
            error: function () {
                console.log("Error deleting address.");
            }
        });
    });

    $("#address").suggestions({
        token: "f066b67c876d948d81ac53beef8fa4191146e8f7", type: "ADDRESS",

        onSelect: function (suggestion) {
            console.log(suggestion);
        }
    });
})


const showPopupBtn = document.getElementById('showPopupBtn');
const addAddressPopup = document.getElementById('addAddressPopup');

if (showPopupBtn && addAddressPopup) {
    showPopupBtn.addEventListener('click', function () {
        addAddressPopup.style.display = 'block';
    });
}

function closePopup() {
    document.getElementById('addAddressPopup').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    const showAllButton = document.getElementById('showAllButton');
    const addresses = document.querySelectorAll('.addresses .address');

    showAllButton.addEventListener('click', function () {
        addresses.forEach(function (address) {
            address.classList.remove('hidden');
        });
        showAllButton.style.display = 'none';
    });
});