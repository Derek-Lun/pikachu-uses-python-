var os = require('os');
var dgram = require('dgram');

var port = 8000;
var client = dgram.createSocket("udp4");
client.bind(port);


var data = {
  used: os.totalmem() - os.freemem(),
  uptime: os.uptime(),
  loadavg: os.loadavg()
}

client.on("message", function (msg, rinfo) {

  if (msg.toString() === "ReplyWithDataPlease") {
    var reply = new Buffer(JSON.stringify(data));

    client.send(reply, 0, reply.length, rinfo.port, rinfo.address, function(err, bytes) {
        if (err) throw err;
        console.log('UDP message sent to ' + rinfo.address +':'+ rinfo.port);
    });
  }

  console.log(msg.toString(), rinfo);

});