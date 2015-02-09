var dgram = require("dgram");
var crypto = require("crypto");
var ping = require('ping');
var LineByLineReader = require('line-by-line');
var _ = require('lodash');
var os = require('os');
 
var port = 5627;
 
var server = dgram.createSocket("udp4");
server.bind(port);

var result = [];
var timeouts = [];

if (process.argv[2] === '-m') {
  var nodes = []

  var lr = new LineByLineReader('listOfNodes.txt');

  lr.on('error', function (err) {

  });

  lr.on('line', function (host) {
    nodes.push(host);
  });

  lr.on('end', function () {
    var tiers = parseInt(process.argv[3])
    if (isNaN(tiers)) {
      process.exit(1);
    }

    hierarchal(nodes, tiers);
  });
}

server.on('listening', function () {
    var address = server.address();
    console.log('UDP Server listening on ' + address.address + ":" + address.port);
});

server.on("message", function (msg, rinfo) {
  var reply = JSON.parse(msg);

  switch(msg.command) {
      case "ReplyWithStatusPlease":
          respondWithStatus(reply);
          break;
      case "RespondedWithData":
          parseStatusResponse(reply, rinfo);
          break;
      default:
          console.log("wrong command")
  }

});

var hierarchal = function (list, tier) {
  var length = Math.ceil(Math.pow(list.length, 1/tiers));

  var groups = _.chunk(list, [size=Math.pow(length, tiers - 1)])

  _.each(groups, function(group) {

  })

  console.log(groups);
}

var getDataFromHost = function (host) {
  var status = {
    hostname: host
  }
  ping.sys.probe(host, function (isAlive) {
      var msg = isAlive ? 'host ' + host + ' is alive' : 'host ' + host + ' is dead';
      status.alive = isAlive;
      var req = JSON.stringify({
        command: "ReplyWithStatusPlease",
        data: status
      });
      var request = new Buffer(req);

      result.push(status);

      if (isAlive) {
        server.send(request, 0, request.length, port, host, function(err, bytes) {
            if (err) throw err;
            console.log('UDP message sent to ' + host +':'+ port);
        })
      }
  });
}


var parseStatusResponse = function (reply, rinfo) {
  var index = _.findIndex(result, {hostname: reply.data.hostname})

  reply.data.ipaddress = rinfo.address;

  if (index !== -1) {
    result[index] = reply.data;
  } else {
    result.push(reply.data);
  }
}

var respondWithStatus = function (request) {
  request.data.used = os.totalmem() - os.freemem();
  request.data.free = os.freemem();
  request.data.uptime = os.uptime();
  request.data.loadavg = os.loadavg();

  request.command = "RespondedWithData"

  var reply = new Buffer(JSON.stringify(request));

  client.send(reply, 0, reply.length, rinfo.port, rinfo.address, function(err, bytes) {
      if (err) throw err;
      console.log('UDP message sent to ' + rinfo.address +':'+ rinfo.port);
  });
}