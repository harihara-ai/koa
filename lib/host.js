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

/**
 * Write a host one way for comparison: lower case, no root dot, no default port.
 * A host the URL parser refuses gives ''.
 *
 * @param {String} host
 * @return {String}
 * @api private
 */

function canonicalHost (host) {
  let url
  try {
    url = new URL(`http://${host}`)
  } catch (e) {
    return ''
  }
  const hostname = stripRootDot(url.hostname)
  return url.port ? `${hostname}:${url.port}` : hostname
}

module.exports = { stripRootDot, canonicalHost }
