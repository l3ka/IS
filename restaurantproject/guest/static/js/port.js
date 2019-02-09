/**
 * Used for asynchronous long polling (BAD simulation of server side events)
 */
const CSRFRegExp = new RegExp('csrftoken=([A-z0-9]+)');
class Port {
    constructor(url) {
        this.url = url;
        this.hooks = {};
    }
    sendMessage(path, params, data, optionsOverride = {}) {
        params = params || {};

        const options = {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json; charset=utf-8'
            }
        };

        if (typeof data === 'object') {
            options.body = JSON.stringify(data);
            options.method = optionsOverride.method || 'POST';
            const csrfTokenMatch = CSRFRegExp.exec(document.cookie),
                csrfToken = csrfTokenMatch && csrfTokenMatch.length == 2 ? csrfTokenMatch[1] : null;
            options.headers = {
                'X-CSRFToken': csrfToken
            };
        }

        let queryString = Object.keys(params).reduce((current, next) => {
            current += `&${next}=${encodeURIComponent(params[next])}`;
            return current;
        }, '');

        queryString = queryString.length > 0 ? '?' + queryString.slice(1, queryString.length) : queryString;
        return fetch(this.url + path + queryString, options);
    }
    removeOnMessageListener(id) {
        if (!this.hooks[id]) {
            return;
        }
        clearInterval(this.hooks[id].intervalId);
        this.hooks[id] = {
            listeners: []
        };
    }
    addOnMessageListener({ id, path, params, data }, callback) {
        if (!this.hooks[id]) {
            this.hooks[id] = {
                listeners: []
            };

            this.hooks[id].intervalId = setInterval(() => {
                this.sendMessage(path, params, data).then((res) => {
                    this.hooks[id].listeners.forEach(listener => {
                        console.log(listener);
                        listener(res);
                    });
                });
            }, 100);
        }
        this.hooks[id].listeners.push(callback);
    }
}

// export default Port;