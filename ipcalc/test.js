#!/usr/bin/env node

// 'test.js'.
// Chris Shiels.


'use strict';


const assert = require('assert');
const ipcalc = require('./ipcalc');
const stringwritable = require('./lib/stringwritable.js');


describe('ipcalc', function() {
  describe('#range()', function() {
    it('returns [ 1..10 ] for range(1, 11)',
       function() {
         assert.deepEqual(ipcalc.range(1, 11),
                          [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]);
    });

    it('returns [ 0,2,4,6,8,10 ] for range(0, 11, 2)',
       function() {
         assert.deepEqual(ipcalc.range(0, 11, 2),
                          [ 0, 2, 4, 6, 8, 10 ]);
    });
  });


  describe('#cidrtowordmask()', function() {
    it('returns [ 0,0 ] for cidrtowordmask("0.0.0.0/0")',
       function() {
         assert.deepEqual(ipcalc.cidrtowordmask("0.0.0.0/0"),
                          [ 0, 0 ]);
    });

    it('returns [ 16909060,8 ] for cidrtowordmask("1.2.3.4/8")',
       function() {
         assert.deepEqual(ipcalc.cidrtowordmask('1.2.3.4/8'),
                          [ 16909060, 8 ]);
    });

    // Note:
    // - In JavaScript bitwise operations operate on signed 32-bit values.
    // - These are represented using two's-compliment for negative numbers.
    // - So 255.255.255.255 = 2^32-1 = -1.
    it('returns [ -1,32 ] for cidrtowordmask("255.255.255.255/32")',
       function() {
         assert.deepEqual(ipcalc.cidrtowordmask('255.255.255.255/32'),
                          [ -1, 32 ]);
    });
  });


  describe('#wordmasktocidr()', function() {
    it('returns "0.0.0.0/0" for wordmasktocidr(...cidrtowordmask("0.0.0.0/0"))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.cidrtowordmask("0.0.0.0/0")),
                      "0.0.0.0/0");
    });

    it('returns "1.2.3.4/8" for wordmasktocidr(...cidrtowordmask("1.2.3.4/8"))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.cidrtowordmask("1.2.3.4/8")),
                      "1.2.3.4/8");
    });

    it('returns "255.255.255.255/32" for wordmasktocidr(...cidrtowordmask("255.255.255.255/32"))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.cidrtowordmask("255.255.255.255/32")),
                      "255.255.255.255/32");
    });
  });


  describe('#networkaddress()', function() {
    it('returns "0.0.0.0/0" for wordmasktocidr(...networkaddress(...cidrtowordmask("0.0.0.0/0")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.networkaddress(
                          ...ipcalc.cidrtowordmask("0.0.0.0/0"))),
                      "0.0.0.0/0");
    });

    it('returns "192.192.0.0/16" for wordmasktocidr(...networkaddress(...cidrtowordmask("192.192.192.192/16")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.networkaddress(
                          ...ipcalc.cidrtowordmask("192.192.192.192/16"))),
                      "192.192.0.0/16");
    });

    it('returns "192.192.192.0/18" for wordmasktocidr(...networkaddress(...cidrtowordmask("192.192.192.192/18")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.networkaddress(
                          ...ipcalc.cidrtowordmask("192.192.192.192/18"))),
                      "192.192.192.0/18");
    });

    it('returns "255.255.255.255/32" for wordmasktocidr(...networkaddress(...cidrtowordmask("255.255.255.255/32")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.networkaddress(
                          ...ipcalc.cidrtowordmask("255.255.255.255/32"))),
                      "255.255.255.255/32");
    });
  });


  describe('#broadcastaddress()', function() {
    it('returns "255.255.255.255/0" for wordmasktocidr(...broadcastaddress(...cidrtowordmask("0.0.0.0/0")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.broadcastaddress(
                          ...ipcalc.cidrtowordmask("0.0.0.0/0"))),
                      "255.255.255.255/0");
    });

    it('returns "192.192.255.255/16" for wordmasktocidr(...broadcastaddress(...cidrtowordmask("192.192.192.192/16")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.broadcastaddress(
                          ...ipcalc.cidrtowordmask("192.192.192.192/16"))),
                      "192.192.255.255/16");
    });

    it('returns "192.192.255.255/18" for wordmasktocidr(...broadcastaddress(...cidrtowordmask("192.192.192.192/18")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.broadcastaddress(
                          ...ipcalc.cidrtowordmask("192.192.192.192/18"))),
                      "192.192.255.255/18");
    });

    it('returns "255.255.255.255/32" for wordmasktocidr(...broadcastaddress(...cidrtowordmask("255.255.255.255/32")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.broadcastaddress(
                          ...ipcalc.cidrtowordmask("255.255.255.255/32"))),
                      "255.255.255.255/32");
    });
  });


  describe('#firsthostaddress()', function() {
    it('returns "0.0.0.1/0" for wordmasktocidr(...firsthostaddress(...cidrtowordmask("0.0.0.0/0")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.firsthostaddress(
                          ...ipcalc.cidrtowordmask("0.0.0.0/0"))),
                      "0.0.0.1/0");
    });

    it('returns "192.192.0.1/16" for wordmasktocidr(...firsthostaddress(...cidrtowordmask("192.192.192.192/16")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.firsthostaddress(
                          ...ipcalc.cidrtowordmask("192.192.192.192/16"))),
                      "192.192.0.1/16");
    });

    it('returns "192.192.192.1/18" for wordmasktocidr(...firsthostaddress(...cidrtowordmask("192.192.192.192/18")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                      ...ipcalc.firsthostaddress(
                        ...ipcalc.cidrtowordmask("192.192.192.192/18"))),
                      "192.192.192.1/18");
    });

    // Note this is an error.
    it('returns "0.0.0.0/32" for wordmasktocidr(...firsthostaddress(...cidrtowordmask("255.255.255.255/32")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.firsthostaddress(
                          ...ipcalc.cidrtowordmask("255.255.255.255/32"))),
                      "0.0.0.0/32");
    });
  });


  describe('#lasthostaddress()', function() {
    // Note this is an error.
    it('returns "255.255.255.254/0" for wordmasktocidr(...lasthostaddress(...cidrtowordmask("0.0.0.0/0")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.lasthostaddress(
                          ...ipcalc.cidrtowordmask("0.0.0.0/0"))),
                      "255.255.255.254/0");
    });

    it('returns "192.192.255.254/16" for wordmasktocidr(...lasthostaddress(...cidrtowordmask("192.192.192.192/16")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.lasthostaddress(
                          ...ipcalc.cidrtowordmask("192.192.192.192/16"))),
                      "192.192.255.254/16");
    });

    it('returns "192.192.255.254/18" for wordmasktocidr(...lasthostaddress(...cidrtowordmask("192.192.192.192/18")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.lasthostaddress(
                          ...ipcalc.cidrtowordmask("192.192.192.192/18"))),
                      "192.192.255.254/18");
    });

    it('returns "255.255.255.254/32" for wordmasktocidr(...lasthostaddress(...cidrtowordmask("255.255.255.255/32")))',
       function() {
         assert.equal(ipcalc.wordmasktocidr(
                        ...ipcalc.lasthostaddress(
                          ...ipcalc.cidrtowordmask("255.255.255.255/32"))),
                      "255.255.255.254/32");
    });
  });


  describe('#subnets()', function() {
    it('returns correct subnets for subnets(...cidrtowordmask("1.2.3.4/24"), 25).map((e) => wordmasktocidr(...e))',
       function() {
         assert.deepEqual(
           ipcalc.subnets(...ipcalc.cidrtowordmask('1.2.3.4/24'),
                            25).map((e) => ipcalc.wordmasktocidr(...e)),
           [
             '1.2.3.0/25',
             '1.2.3.128/25'
           ]
         );
    });

    it('returns correct subnets for subnets(...cidrtowordmask("1.2.3.4/24"), 26).map((e) => wordmasktocidr(...e))',
       function() {
         assert.deepEqual(
           ipcalc.subnets(...ipcalc.cidrtowordmask('1.2.3.4/24'),
                            26).map((e) => ipcalc.wordmasktocidr(...e)),
           [
             '1.2.3.0/26',
             '1.2.3.64/26',
             '1.2.3.128/26',
             '1.2.3.192/26'
           ]
         );
    });

    it('returns correct subnets for subnets(...cidrtowordmask("1.2.3.4/24"), 27).map((e) => wordmasktocidr(...e))',
       function() {
         assert.deepEqual(
           ipcalc.subnets(...ipcalc.cidrtowordmask('1.2.3.4/24'),
                            27).map((e) => ipcalc.wordmasktocidr(...e)),
           [
             '1.2.3.0/27',
             '1.2.3.32/27',
             '1.2.3.64/27',
             '1.2.3.96/27',
             '1.2.3.128/27',
             '1.2.3.160/27',
             '1.2.3.192/27',
             '1.2.3.224/27'
           ]
         );
    });

    it('returns correct subnets for subnets(...cidrtowordmask("1.2.3.4/24"), 28).map((e) => wordmasktocidr(...e))',
       function() {
         assert.deepEqual(
           ipcalc.subnets(...ipcalc.cidrtowordmask('1.2.3.4/24'),
                            28).map((e) => ipcalc.wordmasktocidr(...e)),
           [
             '1.2.3.0/28',
             '1.2.3.16/28',
             '1.2.3.32/28',
             '1.2.3.48/28',
             '1.2.3.64/28',
             '1.2.3.80/28',
             '1.2.3.96/28',
             '1.2.3.112/28',
             '1.2.3.128/28',
             '1.2.3.144/28',
             '1.2.3.160/28',
             '1.2.3.176/28',
             '1.2.3.192/28',
             '1.2.3.208/28',
             '1.2.3.224/28',
             '1.2.3.240/28'
           ]
         );
    });
  });


  describe('#padright()', function() {
    it('returns "          " for padright("", 10, " ")',
       function() {
         assert.equal(ipcalc.padright('', 10, ' '),
                      '          ');
    });

    it('returns "abcde     " for padright("abcde", 10, " ")',
       function() {
         assert.equal(ipcalc.padright('abcde', 10, ' '),
                      'abcde     ');
    });

    it('returns "abcdeabcde" for padright(s, 10, " ")',
       function() {
         let s = 'abcdeabcde';
         assert.equal(ipcalc.padright(s, 10, ' '),
                      s);
    });
  });


  describe('#main()', function() {
    it('outputs usage for no arguments',
       function() {
         let stdout = stringwritable.stringwritable();
         assert.equal(ipcalc.main(null, stdout, null,
                                  [ 'ipcalc.js' ]),
                      0);
         assert.equal(stdout.string(),
                      'Usage:  ipcalc address/mask newmask\n');
    });


    it('outputs details for addressmask',
       function() {
         let stdout = stringwritable.stringwritable();
         assert.equal(ipcalc.main(null, stdout, null,
                                  [ 'ipcalc.js', '192.168.133.0/24' ]),
                      0);
         assert.equal(stdout.string(),
                      '\
network             broadcast           first               last              \
\n\
192.168.133.0/24    192.168.133.255/24  192.168.133.1/24    192.168.133.254/24\
\n');
    });


    it('outputs details for addressmask newmask',
       function() {
         let stdout = stringwritable.stringwritable();
         assert.equal(ipcalc.main(null, stdout, null,
                                  [ 'ipcalc.js', '192.168.133.0/24', '26' ]),
                      0);
         assert.equal(stdout.string(),
                      '\
network             broadcast           first               last              \
\n\
192.168.133.0/26    192.168.133.63/26   192.168.133.1/26    192.168.133.62/26 \
\n\
192.168.133.64/26   192.168.133.127/26  192.168.133.65/26   192.168.133.126/26\
\n\
192.168.133.128/26  192.168.133.191/26  192.168.133.129/26  192.168.133.190/26\
\n\
192.168.133.192/26  192.168.133.255/26  192.168.133.193/26  192.168.133.254/26\
\n');
    });
  });
});
