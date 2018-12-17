/* global $, Port */

// TODO: modifikuj za narudzbe(PLURAL!!!)
let KEY = 'Keyo';
let orderKEY = 'orderKeyo';
let pastOrdersKey = 'pastOrdersKey';
const ordersPort = new Port(`${document.location.protocol}//${document.location.host}`);
const hasStorage = typeof Storage !== 'undefined';

$(document).ready(function () {
    $('#modal-menu').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let title = button.data('title'); // Extract info from data-* attributes
        let description = button.data('description');
        let ingredients = button.data('ingredients');
        let price = button.data('price');
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        let modal = $(this);
        modal.find('.modal-title').text(title);
        modal.find('#item-description-text').val(description);
        $('#item-description-text').scrollTop(0);
        $('#item-ingredients-text').scrollTop(0);
        if (!ingredients) {
            $(modal.find('#item-ingredients-text')).hide();
            $(modal.find('#item-ingredients')).hide();
        } else {
            $(modal.find('#item-ingredients-text')).show();
            $(modal.find('#item-ingredients')).show();
            modal.find('#item-ingredients-text').val(ingredients.replace(/,/g, '\n'));
        }
        modal.find('#badge-price').text(price + 'KM');
        modal.find('#add-button').unbind('click');
        modal.find('#add-button').click(function () {
            if (!hasStorage) {
                return;
            }

            const order = {
                'name': title,
                'price': price,
                'note': '',
                'amount': 1,
                'id': -1
            };

            let orders = localStorage.getItem(KEY);
            let menuItemId = localStorage.getItem(orderKEY) || 0;
            orders = orders ? JSON.parse(orders) : [];
            order.id = menuItemId;
            orders.push(order);
            menuItemId = +menuItemId + 1;
            localStorage.setItem(orderKEY, menuItemId);
            localStorage.setItem(KEY, JSON.stringify(orders));

        });
    });

    $('#modal-order').on('show.bs.modal', function () {
        let orders = hasStorage ? JSON.parse(localStorage.getItem(KEY)) : null;
        if (orders == null) {
            return;
        }
        for (var i in orders) {
            createMenuItemOrdered(orders[i]);
        }
        const modal = $(this);
        modal.find('#close-button').unbind('click');
        modal.find('#close-button').click(function () {
            let myNode = modal.find('#menu-items');
            myNode.empty();
        });
        modal.find('#send-order-button').unbind('click');
        modal.find('#send-order-button').click(function () {
            if (!hasStorage) {
                return;
            }
            // zasad samo obrisi iz localStorage-a, pa kad se bude radilo posalji poruku
            orders = localStorage.getItem(KEY);
            if (orders !== null) {
                let pastOrder = JSON.parse(orders);
                ordersPort.sendMessage('/order/', {}, { order: pastOrder }).then(res =>res.json()).then(response => {
                    // TODO: Process response and handle errors
                    ordersPort.addOnMessageListener({ path: `/order-status/${response.order.id}/`, id: 'order-status' }, async response => {
                        const message = await response.json();
                        if (!message || !message.order) {
                            return;
                        }

                        if (message.order.status === 'READY') {
                            // TODO: Notify 
                            ordersPort.removeOnMessageListener('order-status');
                        }
                    }
                    );
                });
                if (pastOrder.length !== 0) {
                    const pastOrdetTimeObj = {
                        'pastOrder': pastOrder,
                        'time_ordered': Date.now() // kasnije pri prikazu bivsih narudzbi svaku stariju od 24 sata brisem i ne pokazaujem
                    };
                    const pastOrdersJSON = localStorage.getItem(pastOrdersKey);
                    const pastOrders = pastOrdersJSON ? JSON.parse(pastOrdersJSON) : [];
                    pastOrders.push(pastOrdetTimeObj);
                    localStorage.setItem(pastOrdersKey, JSON.stringify(pastOrders));
                }
            }
            // Clear current order
            localStorage.setItem(KEY, JSON.stringify([]));
        });
        // + operator for casting to Number
        let priceSum = orders.reduce((a, b) => +a + +b.price * (+b.amount), 0);
        if (priceSum == 0) {
            $(this).find('#badge-price').hide();
        } else {
            $(this).find('#badge-price').show();
            $(this).find('#badge-price').text(priceSum + 'KM');
        }
    });
    $('#modal-order').on('hidden . bs.modal', function () {
        $(this).find('#menu-items').empty();
    });
    $('#modal-past-orders').on('hidden.b s .modal', function () {
        $(this).find('#past-menu-items-orders').empty();
    });
    $('#modal-past-orders').on('show.bs. m odal ', function () {
        if (hasStorage) {
            const pastOrdersJSON = localStorage.getItem(pastOrdersKey);
            if (pastOrdersJSON == null) {
                return;
            }
            let pastOrders = JSON.parse(pastOrdersJSON) || [];
            let needToUpdate = false;
            const currentTime = Date.now();

            for (var i in pastOrders) {
                if ((Math.abs(currentTime - pastOrders[i].time_ordered) / 36e5) > 24) {
                    needToUpdate = true;
                    continue;
                }

                let fragment = $('#past-menu-items-orders');
                let tempHTML = document.createElement('tr');
                tempHTML.className = 'form-group';

                tempHTML.align = 'center';
                tempHTML.innerHTML = '<td colspan="4"><b style="color: black"> Narudžba ' + (parseInt(i) + 1) + '</b></td>';
                fragment.append(tempHTML);
                for (var j in pastOrders[i].pastOrder) {
                    tempHTML = document.createElement('tr');
                    tempHTML.align = 'center';
                    tempHTML.style = 'align-items: center';
                    const pastMenuItem = pastOrders[i].pastOrder[j];
                    tempHTML.innerHTML = '<td>' + pastMenuItem.name + '</td>' +
                        '<td>' + pastMenuItem.amount + '</td>' +
                        '<td>' + pastMenuItem.price + ' KM</td>' +
                        '<td>' + +pastMenuItem.amount * (+pastMenuItem.price) + ' KM</td>';
                    fragment.append(tempHTML);
                }
                tempHTML = document.createElement('tr');
                tempHTML.align = 'right';
                tempHTML.style = 'align-items: right';
                tempHTML.innerHTML = '<td colspan="4"><b style="color: black">' + pastOrders[i].pastOrder.reduce((a, b) => +a + +b.price * (+b.amount), 0) + ' KM</b></td>';
                fragment.append(tempHTML);
            }

            if (needToUpdate) {
                pastOrders = pastOrders.filter(pastOrder => (Math.abs(currentTime - pastOrder.time_ordered) / 36e5) > 24);
                localStorage.setItem(pastOrdersKey, JSON.stringify(pastOrders));
            }
        }
        const modal = $(this);
        modal.find('#close-button').unbind('click');
        modal.find('#close-button').click(function () {
            let myNode = modal.find('#menu-items');
            myNode.empty();
        });
    });
});

// eslint-disable-next-line no-unused-vars
function addNote(menuItemId) {
    if (!hasStorage) {
        return;
    }
    const ordersJSON = JSON.parse(localStorage.getItem(KEY)) || [];
    // ako je dugme prikazano ne moze biti orders-a da nema
    let prompVal = prompt('Unesite napomenu');
    for (var i in ordersJSON) {
        if (ordersJSON[i].id == menuItemId) {
            ordersJSON[i].note = prompVal;
            break;
        }
    }
    localStorage.setItem(KEY, JSON.stringify(ordersJSON));
}

// eslint-disable-next-line no-unused-vars
function addOrder(order) {
    if (!hasStorage) {
        return;
    }
    const orders = JSON.parse(localStorage.getItem(KEY)) || [];
    orders.push(order);
    localStorage.setItem(KEY, JSON.stringify(orders));
}

// eslint-disable-next-line no-unused-vars
function removeMenuItem(menuItemId) {
    if (!hasStorage) {
        return;
    }
    const orders = JSON.parse(localStorage.getItem(KEY)) || [];
    let index = orders.findIndex(function (o) {
        return o.id == menuItemId;
    });
    if (index !== -1) {
        orders.splice(index, 1);
        let priceSum = orders.reduce((a, b) => +a + +b.price * (+b.amount), 0);
        if (priceSum == 0) {
            $('#badge-price').hide();
            $('#badge-price').show();
        } else {
            $('#badge-price').text(priceSum + 'KM');
        }
    }
    localStorage.setItem(KEY, JSON.stringify(orders));
    let nodeToRemove = document.getElementById('div-menu-item-order-' + menuItemId);
    nodeToRemove.parentNode.removeChild(nodeToRemove);

}

// eslint-disable-next-line no-unused-vars
function updateMenuItemAmount(operation, menuItemId) {
    if (!hasStorage) {
        return;
    }

    let orders = JSON.parse(localStorage.getItem(KEY)) || [];
    let needToBeRemoved = false;
    for (var i in orders) {
        if (orders[i].id != menuItemId) {
            continue;
        }

        if (operation == '-') {
            if (orders[i].amount == 1) {
                needToBeRemoved = true;
                // removeMenuItem(menuItemId) // ako bude 0 ukloni stavku sa narudzbe
            } else {
                orders[i].amount = parseInt(orders[i].amount) - 1;
                $('#input-menu-item-order-' + menuItemId).val(orders[i].amount);
                let priceSum = orders.reduce((a, b) => +a + +b.price * (+b.amount), 0);
                if (priceSum == '0') {
                    $('#badge-price').hide();
                } else {
                    $('#badge-price').show();
                    $('#badge-price').text(priceSum + 'KM');
                }
            }
        } else {
            if (orders[i].amount == '10') { // zasad je hard code 10 kao max val, kad se napravi 
                //baza i popuni promijeniti u broj elemenata na stanju ako je takav tip artikla, ako ne ograniciti na tipa 20 ili sta vec
                window.alert('Ne može se naručiti više artikala ove vrste.');
            } else {
                orders[i].amount = parseInt(orders[i].amount) + 1;
                $('#input-menu-item-order-' + menuItemId).val(orders[i].amount);
                let priceSum = orders.reduce((a, b) => +a + +b.price * (+b.amount), 0);
                if (priceSum == '0') {
                    $('#badge-price').hide();
                } else {
                    $('#badge-price').show();
                    $('#badge-price').text(priceSum + 'KM');
                }
            }
        }
        break;
    }
    if (needToBeRemoved) {
        removeMenuItem(menuItemId);
    } else {
        localStorage.setItem(KEY, JSON.stringify(orders));
    }
}

function createMenuItemOrdered(menuItem) {
    let fragment = $('#menu-items');
    let temp = document.createElement('div');
    temp.className = 'form-group';
    temp.id = 'div-menu-item-order-' + menuItem.id;
    // temp.innerHTML = "<label class=\"col-form-label\" style=\"display: inline-block; border-bottom: groove;\">" + menuItem.name + "</label><div style=\"float:right;\"><input type=\"number\" style=\"display: inline-block; text-align: right; margin-right: 4px\" min=\"1\" max=\"10\" title=\"Količina\" style=\"margin-top: 5px; margin-right: 4px\" value=\"2\"><button type=\"button\" class=\"btn btn-outline-dark btn-sm\" style=\"width:30px; margin-bottom: 5px; margin-right: 4px;\">-</button><button type=\"button\" class=\"btn btn-dark btn-sm\" style=\"width:30px; margin-bottom: 5px; margin-right: 4px\">+</button><button type=\"button\" class=\"btn btn-dark btn-sm\" style=\"width:30px; margin-bottom: 5px; height: 31px !important;\" onclick=\"window.prompt('Unesite napomenu')\"><img style=\" margin-left: -3px !important; height: 18px;\" src=\"{% static 'img/note.png' %}\" alt=\"\"></button></div>";
    temp.innerHTML = `<label class="col-form-label" style="display: inline-block; border-bottom: groove;">${menuItem.name}</label>
        <div style="float:right;">
        <input id="input-menu-item-order-${menuItem.id}" type="number" style="display: inline-block; text-align: right; margin-right: 4px" min="1" max="10"
        title="Količina" style="margin-top: 5px" value="1">
        <button type="button" class="btn btn-outline-dark btn-sm" onclick="updateMenuItemAmount('-', ${menuItem.id})" style="width:30px; margin-bottom: 5px; margin-right: 4px">-</button>
        <button type="button" class="btn btn-dark btn-sm" onclick="updateMenuItemAmount('+', ${menuItem.id})" style="width:30px; margin-bottom: 5px; margin-right: 4px">+</button>
        <button type="button" class="btn btn-outline-dark btn-sm" style="width:30px; margin-bottom: 5px; margin-right: 4px" onclick="addNote(${menuItem.id})"
        title="Dodaj napomenu"><i class="material-icons">note_add</i></button>
        <button type="button" class="btn btn-dark btn-sm" style="width:30px; margin-bottom: 5px;" onclick="removeMenuItem(${menuItem.id})"
        title="Ukloni stavku sa narudžbe"><i class="material-icons">remove_shopping_cart</i></button>
        </div>`;
    fragment.append(temp);
}
