/* global localforage  importScripts */

importScripts('localforage.min.js');
self.addEventListener('message', function (event) {
    const orderId = event.data;
    localforage.setItem('orderId', '' + orderId);
});
self.addEventListener('push', function (e) {
    localforage.getItem('orderId').then(m => {
        const curl = `${self.location.protocol}//${self.location.host}/order-status/${m}/`;
        console.log(curl);
        fetch(curl).then(res => res.json()).then((data) => {
            let state = '';
            let body = '';
            console.log(data);
            switch (data.order.status) {
            case 'CANCELLED':
                state = 'odbijena';
                body = data.order.reason ? `Razlog: ${data.order.reason}` : '';
                break;
            case 'PROCESSING':
                state = 'prihvaćena';
                body = 'Vaša narudđba je prihvaćena i u pripremi je.';
                break;

            case 'READY':
                state = 'spremna';
                body = 'Vaša narudžba je spremna i uskoro ce biti za vašim stolom.';
                break;

            }
            const title = `Vasa narudžba je ${state}`;
            const options = {
                body: body,
                icon: '/static/img/logo.png',
                vibrate: [100, 50, 100],
                data: {
                    dateOfArrival: Date.now(),
                    primaryKey: '2'
                }
            };
            e.waitUntil(
                self.registration.showNotification(title, options)
            );
        });
    });
});