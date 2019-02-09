/* global $, orderStatuses */
const bartenderPort = new Port(`${document.location.protocol}//${document.location.host}`);
const throwOnIncorrectStatus = async (response) => {
    if (!response.success) {
        throw new Error('Action failed');
    }
    return response;
};

$(document).ready(_ => {
    const setPropById = (ids, prop, val) => {
        ids = Array.isArray(ids) ? ids : [ids];
        ids.forEach(element => {
            $(`#${element}`).prop(prop, val);
        });
    };

    const disableButtons = (ids) => {
        setPropById(ids, 'disabled', true);
    };

    const enableButtons = (ids) => {
        setPropById(ids, 'disabled', false);
    };

    debugger;
    [...$('.order-status')].forEach(elem => {
        const orderId = elem.getAttribute('value');
        switch (elem.innerHTML) {
        case orderStatuses.PROCESSING.ID:
            disableButtons(`btn-reject-${orderId}`);
            break;
        case orderStatuses.READY.ID:
            break;
        default:
            break;
        }

    });

    $('#modal-cancel-order-submit').on('click', ({ currentTarget }) => {
        const orderId = $(currentTarget).val();
        const reason = $('#modal-cancel-order-reason').val().replace(/\s{2,}/g, '');
        disableButtons([`btn-accept-${orderId}`, `btn-ready-${orderId}`, `btn-reject-${orderId}`]);
        bartenderPort.sendMessage(`/order/${orderId}/`, {}, { status: orderStatuses.CANCELLED.ID, reason }, { method: 'PATCH' }).then(res => res.json()).then(throwOnIncorrectStatus).then(response => {
            $($(`#btn-accept-${orderId}`).parent()).siblings('.order-status-text').text(orderStatuses.CANCELLED.TEXT);
        }).catch(() => {
            enableButtons([`btn-accept-${orderId}`, `btn-ready-${orderId}`]);
        }).finally(() => {
            $(currentTarget).val('');
            $('#modal-cancel-order-reason').val('');
            $('#modal-cancel-order').hide();
        });

    });

    $('#orders-table').on('click', '.btn-reject', ({ currentTarget }) => {
        const orderId = $(currentTarget).val();
        $('#modal-cancel-order-submit').val(orderId);
        $('#modal-cancel-order').show();
    });
    $('#orders-table').on('click', '.btn-accept', ({ currentTarget }) => {
        const orderId = $(currentTarget).val();
        disableButtons(`btn-reject-${orderId}`);
        bartenderPort.sendMessage(`/order/${orderId}/`, {}, { status: orderStatuses.PROCESSING.ID }, { method: 'PATCH' }).then(res => res.json()).then(throwOnIncorrectStatus).then(response => {
            $($(`#btn-reject-${orderId}`).parent()).siblings('.order-status-text').text(orderStatuses.PROCESSING.TEXT);
        }).catch(() => {
            enableButtons(`btn-reject-${orderId}`);
        });
    });
    $('#orders-table').on('click', '.btn-ready', ({ currentTarget }) => {
        const orderId = $(currentTarget).val();
        disableButtons(`btn-reject-${orderId}`);
        bartenderPort.sendMessage(`/order/${orderId}/`, {}, { status: orderStatuses.READY.ID }, { method: 'PATCH' }).then(res => res.json()).then(throwOnIncorrectStatus).then(response => {
            $($(`#btn-reject-${orderId}`).parent()).siblings('.order-status-text').text(orderStatuses.READY.TEXT);
        }).catch(() => {
            enableButtons(`btn-reject-${orderId}`);
        });
    });
}); 