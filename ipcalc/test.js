#!/usr/bin/env node

// 'test.js'.
// Chris Shiels.


'use strict';


var assert = require('assert');
var ipcalc = require('./ipcalc');


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

    it('returns [ -1,32 ] for cidrtowordmask("255.255.255.255/32")',
       function() {
         assert.deepEqual(ipcalc.cidrtowordmask('255.255.255.255/32'),
                          [ -1, 32 ]);
    });
  });


  describe('#wordmasktocidr()', function() {
    it('returns "0.0.0.0/0" for wordmasktocidr(...cidrtowordmask("0.0.0.0/0"))',
       function() {
         assert.deepEqual(ipcalc.wordmasktocidr(
		            ...ipcalc.cidrtowordmask("0.0.0.0/0")),
                          "0.0.0.0/0");
    });

    it('returns "1.2.3.4/8" for wordmasktocidr(...cidrtowordmask("1.2.3.4/8"))',
       function() {
         assert.deepEqual(ipcalc.wordmasktocidr(
		            ...ipcalc.cidrtowordmask("1.2.3.4/8")),
                          "1.2.3.4/8");
    });

    it('returns "255.255.255.255/32" for wordmasktocidr(...cidrtowordmask("255.255.255.255/32"))',
       function() {
         assert.deepEqual(ipcalc.wordmasktocidr(
		            ...ipcalc.cidrtowordmask("255.255.255.255/32")),
                          "255.255.255.255/32");
    });
  });
});
