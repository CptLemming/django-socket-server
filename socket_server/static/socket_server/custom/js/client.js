var SocketClient = function(uri) {

  return {
    _uri: uri,
    _socket: null,
    _events: {},
    connect: function() {
      this._socket = new WebSocket(this._uri);

      this._socket.onopen = function(event) {
        console.log('onOpen', event);
      };

      this._socket.onclose = function(event) {
        console.log('onClose', event);
      };

      this._socket.onmessage = function(event) {
        var payload = JSON.parse(event.data);
        var event_name = payload['event'];
        delete payload['event'];

        this.fire_callback(event_name, payload);
      }.bind(this);

      this._socket.onerror = function(event) {
        console.log('onError', event);
      };
    },
    on: function(event_name, callback) {
      this._events[event_name] = callback;
    },
    fire_callback: function(event_name, payload) {
      if (this._events[event_name]) {
        this._events[event_name](payload);
      }
    },
    emit: function(event_name, data) {
      data = data || {};
      data['event'] = event_name;
      this._socket.send(JSON.stringify(data));
    }
  };
};
