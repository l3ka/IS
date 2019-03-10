/* global $, Port */


// TODO: modifikuj za narudzbe(PLURAL!!!)
let KEY = 'Keyo';
let orderKEY = 'orderKeyo';
let pastOrdersKey = 'pastOrdersKey';
const ordersPort = new Port(`${document.location.protocol}//${document.location.host}`);
const hasStorage = typeof Storage !== 'undefined';

$(document).ready(function () {
    let fetchMenuItemAdditions = async (menuItemId) => {
        return ordersPort.sendMessage(`/menu/additions/${menuItemId}/`, {}, {}).then(res => res.json());
    };
    $('#modal-call-bartender').on('show.bs.modal', function (event) {
        const tableNumber = sessionStorage.getItem('tableNumber');
        if (!tableNumber) {
            return;
        }
        $('#table-number-select').val(tableNumber);
        $('#call-bartender-table').val(tableNumber);
    });
    $('#call-bartender-button').click(e => {
        const tableNumber = +$('#call-bartender-table').val();
        if (!tableNumber) {
            return;
        }
        sessionStorage.setItem('tableNumber', tableNumber);
        ordersPort.sendMessage('/call-bartender/', {}, { tableNumber }).then(res => res.json()).then(response => {
            console.log(1);
        });
    });
    $('#modal-menu').on('show.bs.modal', function (event) {
        $('.list-group').html('');
        $('#add-item-success').hide();
        $('#add-item-success-row').hide();
        let button = $(event.relatedTarget); // Button that triggered the modal
        let title = button.data('title'); // Extract info from data-* attributes
        let id = button.data('id');
        fetchMenuItemAdditions(id).then(data => {
            const allOptions = JSON.parse(JSON.stringify(data)); // Clone
            let description = button.data('description');
            let ingredients = button.data('ingredients');
            const priceData = {
                _basePrice: 0.0,
                _price: 0.0,
                set basePrice(value) {
                    this._basePrice = value;
                },
                get basePrice() {
                    return this._basePrice;
                },
                set price(value) {
                    this._price = value;
                    modal.find('#badge-price').text((+this._price).toFixed(2) + 'KM');
                },
                get price() {
                    return this._price;
                }
            };
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

            //################### PRILOZI ###################
            const menuItemOptionsContainer = $(this).find('.menu-item-options .list-group');
            const getOptionGroupHTML = (single, options) => {
                let template = '';
                if (single) {
                    template += `<select class='single-option-select'>${
                        options.map(op => {
                            return `<option data-price=${op.price} data-name=${op.name} data-id=${op.id}> ${op.name}   (${op.price} KM) </option>`;
                        }).join('')
                    }</select>`;
                } else {
                    template += '<div class="optional-options-container">' + options.map(o => {
                        return `<div class="optional">
                                    <input type="checkbox" data-price=${o.price} data-name=${o.name} data-id=${o.id}>
                                    <span class=""> ${o.name} </span>
                                </div>`;
                    }).join('') + '</div>';
                }
                return template;
            };

            const mandatoryOptionGroups = data.groups.filter(o => o.required);
            mandatoryOptionGroups.forEach(element => {
                const sample = `<li class="list-group-item menu-item-addition-group" data-id="${o.id}" data-price="0.0">
                                    <span class='menu-item-options-title'> ${element.name} </span>
                                    ${getOptionGroupHTML(element.single, element.options)}
                                </li>`;
                menuItemOptionsContainer.append($(sample));
            });

            const availableOptions = data.groups.filter(o => !o.required);
            const availableOptionsListHTML = `<li class="list-group-item">
                <div class='menu-item-options-addmore' style="display:none">
                    <span>Dodaj Prilog: </span>
                    <select>
                        <option selected></option>
                        ${availableOptions.map(o => `<option>${o.name}</option>`).join('')}
                    </select>
                </div>
            </li>`;

            const updatePrice = () => {
                let priced = [...document.querySelectorAll('.menu-item-options .list-group .list-group-item select option:checked[data-price]')];
                priced = [...priced, ...document.querySelectorAll('.menu-item-options .list-group .list-group-item input:checked[type="checkbox"]')];
                const totalAddidionalPrice = priced.reduce((prev, curr) => {
                    return prev + +$(curr).data('price');
                }, 0);
                priceData.price = +priceData.basePrice + totalAddidionalPrice;
            };

            $(menuItemOptionsContainer).on('change', '.single-option-select', function (e) {
                updatePrice();
            });
            $(menuItemOptionsContainer).on('change', '.list-group-item input', function (e) {
                updatePrice();
            });


            if (availableOptions.length) {

                const addOption = `<li class="list-group-item">
                                    <img src='https://www.nginx.com/wp-content/plugins/nginxcom-plugin-ecommerce/nginx-cart/app/assets/images/nginx-plus-icon.png' width=16 height=16/>
                               </li>`;

                menuItemOptionsContainer.append($(addOption));
                $('.list-group-item img').on('click', e => {
                    $($(e.currentTarget).parent()).hide();
                    $('.menu-item-options-addmore').show();
                });


                menuItemOptionsContainer.append($(availableOptionsListHTML));
                $('.menu-item-options-addmore select').change(function (e) {
                    const selectedIndex = availableOptions.findIndex(o => o.name == this.value);
                    if (selectedIndex === -1) {
                        return;
                    }

                    const selected = availableOptions.splice(selectedIndex, 1)[0];
                    $($(e.currentTarget).find(':selected')).remove();
                    const optionHTML = `<li class="list-group-item menu-item-addition-group" data-id="${selected.id}" data-price="0.0">
                        <span class='menu-item-options-title'> ${selected.name} </span>
                        ${getOptionGroupHTML(selected.single, selected.options)}
                    </li>`;
                    $($(optionHTML)).insertBefore($('.list-group-item img').parent());
                    $('.menu-item-options-addmore').hide();
                    if (availableOptions.length > 0) {
                        $($('.list-group-item img').parent()).show();
                    }
                });
            }


            //################# END PRILOZI ###########################
            priceData.basePrice = button.data('price');
            priceData.price = button.data('price');// @Nedeljko, nisam siguran, da li ce ovo fix, ali trenutno ako ne dodas prilog cijena je 0.00KM
            modal.find('#add-button').unbind('click');
            modal.find('#add-button').click(function () {
                if (!hasStorage) {
                    return;
                }

                modal.find('#add-item-success').show();
                modal.find('#add-item-success-row').show();

                let optionGroupsElements = [...document.querySelectorAll('.menu-item-options .list-group .menu-item-addition-group[data-id]')];
                let options = {
                    groups: []
                };

                for (optionGr of optionGroupsElements) {
                    const ogrid = $(optionGr).data('id');
                    const optionGroupInfo = allOptions.groups.find(o => o.id == ogrid);
                    const selected = [...$(optionGr).find(optionGroupInfo.single ? 'select option:checked[data-id]' : 'input:checked[data-id]')];
                    const selectedInfo = selected.map(s => {
                        const el = $(s);
                        return {
                            name: el.data('name'),
                            id: el.data('id'),
                            price: el.data('price')
                        };
                    });
                    options.groups.push({
                        name: optionGroupInfo.name,
                        id: optionGroupInfo.id,
                        selected: selectedInfo
                    });
                }

                const order = {
                    'name': title,
                    'price': priceData.price,
                    'note': '',
                    'amount': 1,
                    'id': -1,
                    options,
                    pushEndpoint: localStorage.getItem('pushEndpoint')
                };

                let orders = localStorage.getItem(KEY);
                let menuItemId = localStorage.getItem(orderKEY) || 0;
                orders = orders ? JSON.parse(orders) : [];
                order.id = menuItemId;
                orders.push(order);
                menuItemId = +menuItemId + 1;
                localStorage.setItem(orderKEY, menuItemId);
                localStorage.setItem(KEY, JSON.stringify(orders));

                setTimeout(function () {
                    modal.modal('hide');
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                    $('body').css('padding-right', '0px');
                }, 2000);
            });
        });
    });

    $('#modal-order').on('show.bs.modal', function () {
        const tableNumber = sessionStorage.getItem('tableNumber');
        if (tableNumber) {
            $('#table-number-select').val(tableNumber);
        }
        $('#order-modal-error').hide();
        $('#order-modal-error').text('');
        $('#order-modal-success').hide();
        $('#order-modal-success').text('');
        let orderItemsJson = hasStorage ? JSON.parse(localStorage.getItem(KEY)) : null;
        if (orderItemsJson == null) {
            return;
        }
        for (var i in orderItemsJson) {
            createMenuItemOrdered(orderItemsJson[i]);
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
            orderItemsJson = localStorage.getItem(KEY);
            let orderItems = JSON.parse(orderItemsJson);
            const tableNumber = +$('#table-number-select').val();
            if (orderItemsJson !== null && orderItems.length !== 0) {
                ordersPort.sendMessage('/order/', {}, { orderItems: orderItems, tableNumber: tableNumber }).then(res => res.json()).then(response => {
                    // TODO: Process response and handle errors
                    const orderId = +response.order.id;
                    if (Number.isNaN(orderId)) {
                        throw new Error('Invalid order ID');
                    }

                    // If browser supports Service Workers (due to Notification support), allow customer to be notified.
                    if ('serviceWorker' in navigator) {
                        navigator.serviceWorker.register('/sw.js');
                        navigator.serviceWorker.controller.postMessage(response.order.id);
                    }

                    orderItems.id = orderId;
                    orderItems.status = orderStatuses.AWAITING_PROCESSING.ID;

                    if (orderItems.length !== 0) {
                        const pastOrdetTimeObj = {
                            'pastOrder': orderItems,
                            id: orderId,
                            'time_ordered': Date.now() // kasnije pri prikazu bivsih narudzbi svaku stariju od 24 sata brisem i ne pokazaujem
                        };
                        const pastOrdersJSON = localStorage.getItem(pastOrdersKey);
                        const pastOrders = pastOrdersJSON ? JSON.parse(pastOrdersJSON) : [];
                        pastOrders.push(pastOrdetTimeObj);
                        localStorage.setItem(pastOrdersKey, JSON.stringify(pastOrders));
                    }

                    // ordersPort.addOnMessageListener({ path: `/order-status/${response.order.id}/`, id: 'order-status' }, async response => {
                    //     const message = await response.json();
                    //     if (!message || !message.order) {
                    //         return;
                    //     }
                    //     console.log(message.order.status);
                    //     if (message.order.status === orderStatuses.READY.ID) {
                    //         // TODO: Notify 
                    //         ordersPort.removeOnMessageListener('order-status');
                    //     }
                    // }
                    // );
                    localStorage.setItem(KEY, JSON.stringify([]));
                    $('#order-modal-success').text('Uspješno ste poslali narudžbu.');
                    $('#order-modal-success').show();
                }).catch(_ => {
                    $('#order-modal-error').text('Problem kod slanja narudžbe. Molimo pozovite konobara.' + _);
                    $('#order-modal-error').show();
                });
            }
        });
        // + operator for casting to Number
        let priceSum = orderItemsJson.reduce((a, b) => +a + +b.price * (+b.amount), 0);
        if (priceSum == 0) {
            $(this).find('#badge-price').hide();
        } else {
            $(this).find('#badge-price').show();
            $(this).find('#badge-price').text((+priceSum).toFixed(2) + 'KM');
        }
    });
    $('#modal-order').on('hidden.bs.modal', function () {
        $(this).find('#menu-items').empty();
    });
    $('#modal-past-orders').on('hidden.bs.modal', function () {
        $(this).find('#past-menu-items-orders').empty();
    });
    $('#modal-past-orders').on('show.bs.modal', function () {
        if (hasStorage) {
            const pastOrdersJSON = localStorage.getItem(pastOrdersKey);
            if (pastOrdersJSON == null) {
                return;
            }

            let pastOrders = JSON.parse(pastOrdersJSON) || [];
            let needToUpdate = false;
            const currentTime = Date.now();

            for (var i in pastOrders) {
                // if ((Math.abs(currentTime - pastOrders[i].time_ordered) / 36e5) > 24) {
                //     needToUpdate = true;
                //     continue;
                // }
                const orderId = pastOrders[i].id;
                ordersPort.sendMessage(`/order-status/${orderId}/`).then(res => res.json()).then(message => {
                    if (!message || !message.order) {
                        return;
                    }
                    const status = orderStatuses[message.order.status].TEXT;
                    $(`.status-text-${orderId}`).text(status);
                });

                let fragment = $('#past-menu-items-orders');
                let tempHTML = document.createElement('tr');
                tempHTML.className = 'form-group';
                tempHTML.classList.add(`order-info-${orderId}`);

                tempHTML.align = 'center';
                tempHTML.innerHTML = '<tdcolspan="4"><b style="color: black"> Narudžba ' + (parseInt(i) + 1) + '</b></td>';
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
                fragment.append(`<td  colspan="4"><b class="status-text-${orderId}"  style="color: black">GOTOVO</b></td>`);
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
        } else {
            $('#badge-price').text((+priceSum).toFixed(2) + 'KM');
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
                let priceSum = orders.reduce((sum, order) => sum + (+order.price * (+order.amount)), 0);
                if (priceSum == '0') {
                    $('#badge-price').hide();
                } else {
                    $('#badge-price').show();
                    $('#badge-price').text((+priceSum).toFixed(2) + 'KM');
                }
            }
        } else {
            if (orders[i].amount == '10') { // zasad je hard code 10 kao max val, kad se napravi 
                //baza i popuni promijeniti u broj elemenata na stanju ako je takav tip artikla, ako ne ograniciti na tipa 20 ili sta vec
                window.alert('Ne može se naručiti više artikala ove vrste.');
            } else {
                orders[i].amount = parseInt(orders[i].amount) + 1;
                $('#input-menu-item-order-' + menuItemId).val(orders[i].amount);
                console.log(orders);
                let priceSum = orders.reduce((sum, order) => sum + (+order.price * (+order.amount)), 0);
                if (priceSum == '0') {
                    $('#badge-price').hide();
                } else {
                    $('#badge-price').show();
                    $('#badge-price').text((+priceSum).toFixed(2) + 'KM');
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
