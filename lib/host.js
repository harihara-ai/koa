'use strict'

/**
 * Drop the trailing root dot of a host name (`example.com.` is `example.com`).
 *
 * @param {String} hostname
 * @return {String}
 * @api private
 */

function stripRootDot (hostname) {
  return hostname.endsWith('.') ? hostname.slice(0, -1) : hostname
}

module.exports = { stripRootDot }
