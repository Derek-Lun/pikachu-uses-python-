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

  var request = JSON.parse(msg);

  if (request.command === "ReplyWithStatusPlease") {

    request.data.used = os.totalmem() - os.freemem();
    request.data.free = os.freemem();
    request.data.uptime = os.uptime();
    request.data.loadavg = os.loadavg();
    
    var reply = new Buffer(JSON.stringify(request));

    client.send(reply, 0, reply.length, rinfo.port, rinfo.address, function(err, bytes) {
        if (err) throw err;
        console.log('UDP message sent to ' + rinfo.address +':'+ rinfo.port);
    });
  }


});