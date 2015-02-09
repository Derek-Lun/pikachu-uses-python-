var dgram = require("dgram");
var crypto = require("crypto");
var ping = require('ping');
var LineByLineReader = require('line-by-line');
var _ = require('lodash');
var os = require('os');
var async = require('async');
 
var port = 5627;
 
var server = dgram.createSocket("udp4");
server.bind(port);

var result = [];
var timeouts = [];

var master = !!process.argv[2]

if (master) {
  var nodes = []

  var lr = new LineByLineReader('listOfNodes.txt');

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

  switch(reply.command) {
      case "ReplyWithStatusPlease":
          respondWithStatus(reply, rinfo);
          break;
      case "RespondedWithData":
          parseStatusResponse(reply, rinfo);
          break;
      case "ContactGroupToGetStatus":
          hierarchal(reply.data, reply.tier);
      default:
          console.log("wrong command");
  }

});

var hierarchal = function (list, tier) {
  if (tier <= 1) {
    _.each(list, function (host) {
      getDataFromHost(host);
    })
  } else {
    var length = Math.ceil(Math.pow(list.length, 1/tier));

    var groups = _.chunk(list, [size=Math.pow(length, tier - 1)])

    var sub_master = async.map(groups, function(group, done) {
      async.detect(group, function (host, callback) {
        ping.sys.probe(host, function (isAlive) {
          callback(isAlive);
        });
      }, function (result) {
        done(null, result);
      });
    }, function (err, results) {
      _.each(results, function (submaster, index) {
        if (submaster){
          getDataFromHost(submaster, groups[index], tier-1);
        } else {
          entireBranchisDead(groups[index]);
        }
      });
    });
  }

}


var entireBranchisDead = function (grouplist) {
  _.each(grouplist, function (host) {
    result.push({
      hostname: host,
      alive: false
    });
  })
}

var getDataFromHost = function (host, grouplist, tier) {
  var status = {
    hostname: host
  }
  ping.sys.probe(host, function (isAlive) {
      var msg = isAlive ? 'host ' + host + ' is alive' : 'host ' + host + ' is dead';
      var req = {}
      status.alive = isAlive;
      if (grouplist) {
        req = {
          command: "ContactGroupToGetStatus",
          data: grouplist,
          tier: tier
        }
      } else {
        req = {
          command: "ReplyWithStatusPlease",
          data: status
        };
      }

      var request = new Buffer(JSON.stringify(req));

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

var respondWithStatus = function (request, rinfo) {
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