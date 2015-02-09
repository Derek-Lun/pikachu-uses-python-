var dgram = require("dgram");
var crypto = require("crypto");
var ping = require('ping');
var LineByLineReader = require('line-by-line');
var _ = require('lodash');
var os = require('os');
var async = require('async');
var dns = require('dns');
 
var port = 5627;
 
var server = dgram.createSocket("udp4");
server.bind(port);

var result = [];
var timeout;
var timeout_period;
var min_timeout = 1000;

var parent_host;
var parent_port;

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

    var grpnum = Math.ceil(Math.pow(list.length, 1/tier));

    hierarchal(nodes, tiers, grpnum);
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
          hierarchal(reply.data, reply.tier, reply.grpnum, rinfo);
      default:
          console.log("wrong command");
  }

});

var hierarchal = function (list, tier, grpnum, rinfo) {

  parent_host = rinfo.address;
  parent_port = rinfo.port;

  if (tier <= 1) {
    _.each(list, function (host) {
      getDataFromHost(host);
    })
  } else {
    timeout_period = min_timeout * tier;

    var grouplength = Math.ceil(list / grpnum);
    var groups = _.chunk(list, [size=grouplength])

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
          getDataFromHost(submaster, groups[index], tier-1, grpnum);
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

var sendDataBackToParent = function () {
  var current = {}

  current.data.used = os.totalmem() - os.freemem();
  current.data.free = os.freemem();
  current.data.uptime = os.uptime();
  current.data.loadavg = os.loadavg();


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
          tier: tier,
          grpnum: grpnum
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

            if (timeout) {
              clearTimeout(timeout) 
            }

            timeout = setTimeout(function(){ alert("Hello"); }, 1000);
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

  server.send(reply, 0, reply.length, rinfo.port, rinfo.address, function(err, bytes) {
      if (err) throw err;
      console.log('UDP message sent to ' + rinfo.address +':'+ rinfo.port);
  });
}