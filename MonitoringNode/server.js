var dgram = require("dgram");
var crypto = require("crypto");
var ping = require('ping');
var LineByLineReader = require('line-by-line');
 
var port = 5627;
 
var server = dgram.createSocket("udp4");
server.bind(port);

var sendMeData = new Buffer('ReplyWithDataPlease');

server.on('listening', function () {
    var address = server.address();
    console.log('UDP Server listening on ' + address.address + ":" + address.port);
});

server.on("message", function (msg, rinfo) {

  console.log(msg.toString(), rinfo);

});

var lr = new LineByLineReader('listOfNodes.txt');

lr.on('error', function (err) {
    // 'err' contains error object
});

lr.on('line', function (host) {
    console.log(host);
    ping.sys.probe(host, function(isAlive){
        var msg = isAlive ? 'host ' + host + ' is alive' : 'host ' + host + ' is dead';
        console.log(msg);
        if (isAlive) {
          server.send(sendMeData, 0, sendMeData.length, 8000, host, function(err, bytes) {
              if (err) throw err;
              console.log('UDP message sent to ' + host +':'+ 8000);
          })
        }
    });
});

lr.on('end', function () {
    // All lines are read, file is closed now.
});
