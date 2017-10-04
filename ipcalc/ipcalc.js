#!/usr/bin/env node

// 'ipcalc.js'.
// Chris Shiels.


'use strict';


const range = function(start, end, step = 1) {
  if (start >= end)
    return [];
  else
    return [ start ].concat(range(start + step, end, step));
}


const cidrtowordmask = function(s) {
  let re =
    /([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\/([0-9]{1,2})/;
  let matches = s.match(re);
  let [ octet1, octet2, octet3, octet4, mask ] =
    matches.slice(1).map((e) => { return parseInt(e, 10); });
  let word = (octet1 << 24) | (octet2 << 16) | (octet3 << 8) | octet4;
  return [ word, mask ];
}


const wordmasktocidr = function(word, mask) {
  let octets = [
    // Note:
    // - In JavaScript bitwise operations operate on signed 32-bit values.
    // - These are represented using two's-compliment for negative numbers.
    // - So 255.255.255.255 = 2^32-1 = -1 and we use '>>>' to handle this.
    (word >>> 24) & 255,
    (word >> 16) & 255,
    (word >> 8) & 255,
    word & 255
  ];
  return octets.join('.') + '/' + mask;
}


const networkaddress = function(word, mask) {
  return [ word & (Math.pow(2, mask) - 1) << (32 - mask), mask ];
}


const broadcastaddress = function(word, mask) {
  return [ networkaddress(word, mask)[0] | (Math.pow(2, 32 - mask) - 1), mask ];
}


const firsthostaddress = function(word, mask) {
  return [ networkaddress(word, mask)[0] + 1, mask ];
}


const lasthostaddress = function(word, mask) {
  return [ broadcastaddress(word, mask)[0] - 1, mask ];
}


const subnets = function(word, mask, newmask) {
  let step = Math.pow(2, 32 - newmask);
  return range(networkaddress(word, mask)[0],
	       broadcastaddress(word, mask)[0] + 1,
	       step).map((e) => { return [ e, newmask ]; });
}


const ipcalc = function(stdin, stdout, stderr, argv) {
  console.log(subnets(...cidrtowordmask('1.2.3.1/24'),
	              25).map((e) => wordmasktocidr(...e)));
  console.log(subnets(...cidrtowordmask('1.2.3.1/24'),
	              26).map((e) => wordmasktocidr(...e)));
  console.log(subnets(...cidrtowordmask('1.2.3.1/24'),
	              27).map((e) => wordmasktocidr(...e)));
  console.log(subnets(...cidrtowordmask('1.2.3.1/24'),
	              28).map((e) => wordmasktocidr(...e)));
  return 0;
}


//process.exitCode = ipcalc(process.stdin,
//                          process.stdout,
//                          process.stderr,
//                          process.argv.slice(1));


module.exports = {
  'range':            range,
  'cidrtowordmask':   cidrtowordmask,
  'wordmasktocidr':   wordmasktocidr,
  'networkaddress':   networkaddress,
  'broadcastaddress': broadcastaddress,
  'firsthostaddress': firsthostaddress,
  'lasthostaddress':  lasthostaddress
};
