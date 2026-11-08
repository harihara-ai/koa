'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const request = require('../../test-helpers/context').request

describe('req.ips', () => {
  describe('when X-Forwarded-For is present', () => {
    describe('and proxy is not trusted', () => {
      it('should be ignored', () => {
        const req = request()
        req.app.proxy = false
        req.header['x-forwarded-for'] = '127.0.0.1,127.0.0.2'
        assert.deepStrictEqual(req.ips, [])
      })
    })

    describe('and proxy is trusted', () => {
      it('should be used', () => {
        const req = request()
        req.app.proxy = true
        req.header['x-forwarded-for'] = '127.0.0.1,127.0.0.2'
        assert.deepStrictEqual(req.ips, ['127.0.0.1', '127.0.0.2'])
      })
    })
  })

  describe('when options.proxyIpHeader is present', () => {
    describe('and proxy is not trusted', () => {
      it('should be ignored', () => {
        const req = request()
        req.app.proxy = false
        req.app.proxyIpHeader = 'x-client-ip'
        req.header['x-client-ip'] = '127.0.0.1,127.0.0.2'
        assert.deepStrictEqual(req.ips, [])
      })
    })

    describe('and proxy is trusted', () => {
      it('should be used', () => {
        const req = request()
        req.app.proxy = true
        req.app.proxyIpHeader = 'x-client-ip'
        req.header['x-client-ip'] = '127.0.0.1,127.0.0.2'
        assert.deepStrictEqual(req.ips, ['127.0.0.1', '127.0.0.2'])
      })
    })
  })

  describe('when options.maxIpsCount is present', () => {
    describe('and proxy is not trusted', () => {
      it('should be ignored', () => {
        const req = request()
        req.app.proxy = false
        req.app.maxIpsCount = 1
        req.header['x-forwarded-for'] = '127.0.0.1,127.0.0.2'
        assert.deepStrictEqual(req.ips, [])
      })
    })

    describe('and proxy is trusted', () => {
      it('should be used', () => {
        const req = request()
        req.app.proxy = true
        req.app.maxIpsCount = 1
        req.header['x-forwarded-for'] = '127.0.0.1,127.0.0.2'
        assert.deepStrictEqual(req.ips, ['127.0.0.2'])
      })
    })
  })
  describe('REQ-REQ-003: an IPv4 entry with a port', () => {
    it('REQ-REQ-003 happy: drops the port of an IPv4 entry', () => {
      const req = request()
      req.app.proxy = true
      req.header['x-forwarded-for'] = '23.243.1.1:38242, 10.0.0.1'
      assert.deepStrictEqual(req.ips, ['23.243.1.1', '10.0.0.1'])
    })

    it('REQ-REQ-003 edge: returns invalid entries unchanged', () => {
      const req = request()
      req.app.proxy = true
      req.header['x-forwarded-for'] = '1.2.3.4:abc, host.example:80, unknown'
      assert.deepStrictEqual(req.ips, ['1.2.3.4:abc', 'host.example:80', 'unknown'])
    })
  })
})
