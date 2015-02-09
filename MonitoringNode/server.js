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

var sentTo = [];

var master = !!process.argv[2]

if (master) {
  var nodes = []

  var lr = new LineByLineReader('listOfNodes.txt');

  lr.on('line', function (host) {
    nodes.push(host);
  });

  lr.on('end', function () {
    setInterval(function(){ start() }, 300000);
  });
}

var start = function () {
  var tiers = parseInt(process.argv[3])
  if (isNaN(tiers)) {
    process.exit(1);
  }

  var grpnum = Math.ceil(Math.pow(list.length, 1/tier));

  hierarchal(nodes, tiers, grpnum);
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
      case "RespondedWithDataFromGroup":  
          conglomerateData(reply, rinfo);
      default:
          console.log("wrong command");
  }

});

var conglomerateData = function (reply, rinfo) {
  _.each(reply.data, function (rep) {
    if (_.some(sentTo, rep.hostname)) {
      rep.ipaddress = rinfo.address;
    }
    result.push(rep);
  })
}

var hierarchal = function (list, tier, grpnum, rinfo) {
  if (rinfo) {
    parent_host = rinfo.address;
    parent_port = rinfo.port;    
  }

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
          getDataFromHosts(submaster, groups[index], tier-1, grpnum);
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

var getDataFromHosts = function(host, grouplist, tier) {
  var status = {
    hostname: host
  }

  ping.sys.probe(host, function (isAlive) {
      var msg = isAlive ? 'host ' + host + ' is alive' : 'host ' + host + ' is dead';
      var req = {}
      status.alive = isAlive;

      req = {
        command: "ContactGroupToGetStatus",
        grouplist: grouplist,
        tier: tier,
        grpnum: grpnum,
        data: status
      }

      var request = new Buffer(JSON.stringify(req));

      result.push(status);

      if (isAlive) {
        serverSend(request, host, port, timeout_length);
      }
  });
}

var getDataFromHost = function (host) {
  var status = {
    hostname: host
  }

  ping.sys.probe(host, function (isAlive) {
      var msg = isAlive ? 'host ' + host + ' is alive' : 'host ' + host + ' is dead';
      var req = {}
      status.alive = isAlive;

      req = {
        command: "ReplyWithStatusPlease",
        data: status
      };

      var request = new Buffer(JSON.stringify(req));

      result.push(status);

      if (isAlive) {
        serverSend(request, host, port, timeout_length);
      }
  });
}

var timeout_function = function (host) {
  if (parent_port && parent_host) {
    var currentMachine = {
      hostname: host,
      alive: true
    }

    var status = currentMachineStatus()

    currentMachine.used = status.used;
    currentMachine.free = status.free;
    currentMachine.uptime = status.uptime;
    currentMachine.loadavg = status.loadavg;

    result.push(currentMachine);

    var res = {
      command: "RespondedWithDataFromGroup",
      data: result
    }

    var reply = new Buffer(JSON.stringify(res));

    serverSend(reply, parent_host, parent_port);

  } else {
    writeResultToFile();
  }
}

var writeResultToFile = function () {
  var res = JSON.stringify(result);

  console.log(res);

  //inside sutffdnkjagdhgkaghdklghadkl;had;
}

var parseStatusResponsefromHost = function (reply, rinfo) {
  var index = _.findIndex(result, {hostname: reply.data.hostname});

  reply.data.ipaddress = rinfo.address;

  if (index !== -1) {
    result[index] = reply.data;
  } else {
    result.push(reply.data);
  }
}

var currentMachineStatus = function () {
  return {
    used: os.totalmem() - os.freemem(),
    free: os.freemem(),
    uptime: os.uptime(),
    loadavg: os.loadavg()
  }
}

var respondWithStatus = function (request, rinfo) {
  var status = currentMachineStatus();
  request.data.used = status.used;
  request.data.free = status.free;
  request.data.uptime = status.uptime;
  request.data.loadavg = status.loadavg;

  request.command = "RespondedWithData"

  var reply = new Buffer(JSON.stringify(request));

  serverSend(reply, rinfo.address, rinfo.port, min_timeout);
} 

var serverSend = function (messageBuffer, destHost, destPort, timeout_length) {
  sentTo.push(destHost); 
  server.send(messageBuffer, 0, messageBuffer.length, destPort, destHost, function(err, bytes) {
      if (err) throw err;
      console.log('UDP message sent to ' + rinfo.address +':'+ rinfo.port);
  });
}