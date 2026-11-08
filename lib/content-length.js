'use strict'

/**
 * Parse a Content-Length header value (RFC 9110 8.6: digits only).
 *
 * @param {String|Number|undefined} value
 * @return {Number|undefined} the length, or undefined when absent or malformed
 * @api private
 */

module.exports = function parseContentLength (value) {
  const len = String(value).trim()
  return /^\d+$/.test(len) ? Number(len) : undefined
}
