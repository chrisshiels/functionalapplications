#!/usr/bin/env node

// 'ipcalc.js'.
// Chris Shiels.


'use strict';


const util = require('util');


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
  if (matches === null)
    return null;
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


const padright = function(s, len, c = ' ') {
  if (s.length >= len)
    return s;
  else
    return padright(s + c, len, c);
}


const outputnetworkdetailsheader = function(stdout) {
  stdout.write(util.format('%s  %s  %s  %s\n',
                           padright('network', 18),
                           padright('broadcast', 18),
                           padright('first', 18),
                           padright('last', 18)));
  return 0;
}


const outputnetworkdetails = function(stdout, word, mask) {
  let network = wordmasktocidr(...networkaddress(word, mask));
  let broadcast = wordmasktocidr(...broadcastaddress(word, mask));
  let first = wordmasktocidr(...firsthostaddress(word, mask));
  let last = wordmasktocidr(...lasthostaddress(word, mask));
  stdout.write(util.format('%s  %s  %s  %s\n',
                           padright(network, 18),
                           padright(broadcast, 18),
                           padright(first, 18),
                           padright(last, 18)));
  return 0;
}


const outputusage = function(stdout) {
  stdout.write('Usage:  ipcalc address/mask [ newmask ]\n');
  return 0;
}


const main = function(stdin, stdout, stderr, argv) {
  if (argv.length !== 2 && argv.length !== 3) {
    outputusage(stdout);
    return 0;
  }

  let wordmask = cidrtowordmask(argv[1]);
  if (wordmask === null) {
    stderr.write('Error:  Cannot parse address.\n');
    return 1;
  }

  let newmask = wordmask[1];
  if (argv.length === 3)
    newmask = parseInt(argv[2], 10);
  if (isNaN(newmask)) {
    stderr.write('Error:  Cannot parse newmask.\n');
    return 1;
  }

  outputnetworkdetailsheader(stdout);
  for (let subnet of subnets(...wordmask, newmask))
    outputnetworkdetails(stdout, ...subnet);

  return 0;
}


if (!module.parent)
  process.exitCode = main(process.stdin,
                          process.stdout,
                          process.stderr,
                          process.argv.slice(1));
else
  module.exports = {
    'range':            range,
    'cidrtowordmask':   cidrtowordmask,
    'wordmasktocidr':   wordmasktocidr,
    'networkaddress':   networkaddress,
    'broadcastaddress': broadcastaddress,
    'firsthostaddress': firsthostaddress,
    'lasthostaddress':  lasthostaddress,
    'subnets':          subnets,
    'padright':         padright,
    'main':             main
  };
