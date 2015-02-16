var dgram = require("dgram");
var crypto = require("crypto");
 
var hashType = 'sha256';
 
var port = 5627;
 
var server = dgram.createSocket("udp4");
server.bind(port);
 
server.on("message", function (msg, rinfo) {
  var client = {
    ip: msg.readUInt32LE(0),
    srcPort: msg.readUInt16LE(4),
    time: parseInt(msg.readUInt32LE(12).toString(16) + msg.readUInt32LE(8).toString(16), 16),
    id: new Buffer(msg.toString('utf8', 16))
  };
 
  console.log(client)
  console.log(rinfo.address, rinfo.port)
  // Increment secret by 1
  client.id.writeUInt8((client.id).readUInt8(client.id.length-1) + 1, client.id.length-1);
 
  if(Math.random() < 0.4){
    // make & send a response
    var response = new Buffer(100);
    var secret = crypto.createHash(hashType).update(client.id.toString(), 'utf8').digest('hex');
 
    var secretBuffer = new Buffer(secret, "hex");
 
    msg.copy(response, 0, 0, 16); // unique ID
    response.writeUInt32LE(secretBuffer.length, 16); // secret length
    
    secretBuffer.copy(response, 20); // sha1 digest of id
    
    server.send(response, 0, response.length, rinfo.port, rinfo.address);
  }
});