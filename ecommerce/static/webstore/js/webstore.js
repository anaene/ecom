function updatePrice(elem) {
    let orderProductId = elem.id;
    let quantity = elem.value;
    const subtotalElem = $('#subtotal_' + orderProductId);
    const totalElem = $('#total');
    let updateUrl = elem.getAttribute('data-url');
    $.ajax({
        url: updateUrl,
        data: {'orderProductId': orderProductId, 'quantity': quantity},
        success: function (data) {
            subtotalElem.text(data['subtotal']);
            totalElem.text(data['total']);
        }
    })
}

function getAddress(elem) {
    if (elem.checked === true) {
        $.ajax({
            url: '/address/',
            success: function (data) {
                $('#id_street').val(data['street']);
                $('#id_postcode').val(data['postcode']);
                $('#id_city').val(data['city']);
            }
        })
    } else {
        $('#id_street').val('');
        $('#id_postcode').val('');
        $('#id_city').val('');
    }
}