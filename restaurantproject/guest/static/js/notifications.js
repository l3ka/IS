
const requireNotificationPermissions = () => {
    return new Promise((r, e) => {
        Notification.requestPermission(status => {
            if (status === 'granted') {
                r(status);
            }
            e(status);
        });
    });
};

async function init() {
    try {
        await requireNotificationPermissions();
        console.log('INITALIZED NOTIFICATIONS');
        if (Notification.permission == 'granted') {
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/sw.js').then(function (reg) {
                    console.log('Service Worker Registered!', reg);

                    reg.pushManager.getSubscription().then(function (sub) {
                        if (sub === null) {
                            reg.pushManager.subscribe({
                                userVisibleOnly: true
                            }).then(function (sub) {
                                console.log('Endpoint URL: ', sub.endpoint);
                            }).catch(function (e) {
                                if (Notification.permission === 'denied') {
                                    console.warn('Permission for notifications was denied');
                                } else {
                                    console.error('Unable to subscribe to push', e);
                                }
                            });
                        } else {
                            console.log('Subscription object: ', sub);
                            localStorage.setItem('pushEndpoint', sub.endpoint);
                        }
                    });
                })
                    .catch(function (err) {
                        console.log('Service Worker registration failed: ', err);
                    });
            }
        }
    } catch (e) {
        console.log(e);
    }

}


init();