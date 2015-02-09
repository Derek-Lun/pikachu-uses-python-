var dgram = require("dgram");
var crypto = require("crypto");
var ping = require('ping');
var LineByLineReader = require('line-by-line');
var _ = require('lodash');
 
var port = 5627;
 
var server = dgram.createSocket("udp4");
server.bind(port);

var result = []

server.on('listening', function () {
    var address = server.address();
    console.log('UDP Server listening on ' + address.address + ":" + address.port);
});

server.on("message", function (msg, rinfo) {
  var reply = JSON.parse(msg);

  var index = _.findIndex(result, {hostname: reply.data.hostname})

  if (index !== -1) {
    result[index] = reply.data;
  } else {
    result.push(reply.data);
  }

});

var lr = new LineByLineReader('listOfNodes.txt');

lr.on('error', function (err) {
    // 'err' contains error object
});

lr.on('line', function (host) {
    var status = {
      hostname: host
    }
    ping.sys.probe(host, function(isAlive){
        var msg = isAlive ? 'host ' + host + ' is alive' : 'host ' + host + ' is dead';
        status.alive = isAlive;
        var req = JSON.stringify({
          command: "ReplyWithStatusPlease",
          data: status
        });
        var request = new Buffer(req);

        result.push(status);

        if (isAlive) {
          server.send(request, 0, request.length, 8000, host, function(err, bytes) {
              if (err) throw err;
              console.log('UDP message sent to ' + host +':'+ 8000);
          })
        }
    });
});
