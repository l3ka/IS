/* global $, orderStatuses */
const bartenderPort = new Port(`${document.location.protocol}//${document.location.host}`);
const throwOnIncorrectStatus = async (response) => {
    if (!response.success) {
        throw new Error('Action failed');
    }
    return response;
};

const getDishHTML = (order, dish) => {
    const dishHtml = `<tr align="center" class="collapse collapse-${order.id}">
            <td>&nbsp;</td>
            <td> ${ dish.name}</td>
            <td>${ dish.additions}</td>
            <td> ${ dish.price} KM</td>
            <td> ${ dish.quantity} </td>
            <td> ${ dish.note} </td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>`;
    return dishHtml;
};
const getOrderHTML = (order) => {
    let dishes = '';
    for (let dish of order.details) {
        dishes += getDishHTML(order, dish);
    }

    let date = order.time_ordered.split("T")[0].split("-");
    let time = order.time_ordered.split("T")[1].split(":");

    // skida vodece nule regex
    let time_ordered = new Date(+(date[0].replace(/^0+/, '')), +(date[1].replace(/^0+/, '')) - 1, +(date[2].replace(/^0+/, '')),
     +(time[0].replace(/^0+/, '')) + 1, +(time[1].replace(/^0+/, '')), +(time[2].replace("Z", "").replace(/^0+/, '')));

    time_ordered = time_ordered.toLocaleString();

    const orderTemplate = `
    <tr align="center" style="align-items: center">
        <span class='order-status' style="display:none" value="${order.id}">${order.status}</span>
        <td>${ order.table_number}</td>
        <td class='order-status-text'>${ order.status_text}</td>
        <td>${time_ordered}</td>
        <td>${ order.price_together} KM</td>

        <td><button type="button" value="${order.id}" id="btn-reject-${order.id}" data-toggle="modal" data-target="#modal-cancel-order" class="btn btn-outline-danger btn-sm btn-reject">Odbij</button></td>
        <td><button type="button" value="${order.id}" id="btn-accept-${order.id}" class="btn btn-outline-success btn-sm btn-accept">Prihvati</button></td>
        <td><button type="button" value="${order.id}" id="btn-ready-${order.id}" class="btn btn-outline-primary btn-sm btn-ready">Narudžba
                    gotova</button></td>
        <td><button type="button" value="${order.id}" data-toggle="collapse" data-target=".collapse-${order.id}"
            class="btn btn-outline-info btn-sm">Detalji</button></td>
    </tr>

    <div class="colapsed_class">

        <tr align="center" class="collapse collapse-${ order.id}" style="background:#212529">
            <th scope="col" style="color: white">&nbsp;</td>
            <th scope="col"><b>Naziv</b></td>
            <th scope="col"><b>Prilozi</b></td>
            <th scope="col"><b>Cijena</b></td>
            <th scope="col"><b>Količina</b></td>
            <th scope="col"><b>Napomena</b></td>
            <th scope="col">&nbsp;</td>
            <th scope="col">&nbsp;</th>
        </tr>
        ${dishes}
    </div>`;
    return orderTemplate;
};

let lastOrderTime = '';
const getOrder = () => {
    console.log(new Date(lastOrderTime).getTime());
    fetch(`/bartender/orders/?t=${new Date(lastOrderTime).getTime()}`).then(res => res.json()).then(r => {
        for (let order of r.orders) {
            $('.orders-content').append($(getOrderHTML(order)));
        }
        if (r.orders.length > 0) {
            lastOrderTime = r.orders.map(o => o.time_ordered).sort().reverse()[0];
        }
    });
};
setInterval(getOrder, 2000);
getOrder();

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
            setTimeout(() => {
                $($($(`#btn-accept-${orderId}`).parent()).parent()).remove();
                $(`.collapse-${orderId}`).remove();
            }, 3E4);
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
        console.log(`btn-accept-${orderId}`);
        disableButtons([`btn-reject-${orderId}`, `btn-accept-${orderId}`]);
        bartenderPort.sendMessage(`/order/${orderId}/`, {}, { status: orderStatuses.READY.ID }, { method: 'PATCH' }).then(res => res.json()).then(throwOnIncorrectStatus).then(response => {
            $($(`#btn-reject-${orderId}`).parent()).siblings('.order-status-text').text(orderStatuses.READY.TEXT);
            // TODO: BEFORE-AFTER

            // BEFORE
            /*
            setTimeout(() => {
                $($($(`#btn-accept-${orderId}`).parent()).parent()).remove();
                $(`.collapse-${orderId}`).remove();
            }, 3E4);
            */

            // AFTER
            $($($(`#btn-accept-${orderId}`).parent()).parent()).remove();
            $(`.collapse-${orderId}`).remove();

        }).catch(() => {
            enableButtons(`btn-reject-${orderId}`);
        });
    });
    // $('#modal-cancel-order').on('click', ['.close', '.close-modal'], () => {
    //     $('#modal-cancel-order').hide();
    //     $('#modal-cancel-order-reason').val('');
    // });
    $('#modal-cancel-order-submit').on('click', function () {
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $('body').css('padding-right', '0px');
    });
}); 