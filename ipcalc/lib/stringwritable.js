// 'lib/stringwritable.js'.
// Chris Shiels.


'use strict';


const stream = require('stream');


const stringwritable = function() {
  let _stream = new stream.Writable();
  let _chunks = [];

  _stream._write = function(chunk, encoding, callback) {
    _chunks.push(chunk);
    callback();
  }

  _stream.string = function() {
    return _chunks.join('');
  }

  return _stream;
}


module.exports = {
  stringwritable: stringwritable
}
