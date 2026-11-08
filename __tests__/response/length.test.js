'use strict'

const { describe, it } = require('node:test')
const response = require('../../test-helpers/context').response
const assert = require('node:assert/strict')
const fs = require('fs')

describe('res.length', () => {
  describe('when Content-Length is defined', () => {
    it('REQ-RES-004 happy: digits only give the number', () => {
      const res = response()
      res.set('Content-Length', '1024')
      assert.strictEqual(res.length, 1024)
    })

    it('REQ-RES-004 error: a value that is not a number gives undefined', () => {
      const res = response()
      res.set('Content-Length', 'hey')
      assert.strictEqual(res.length, undefined)
    })

    it('REQ-RES-004 error: digits then junk give undefined', () => {
      const res = response()
      res.set('Content-Length', '10abc')
      assert.strictEqual(res.length, undefined)
    })
  })

  describe('when Content-Length is not defined', () => {
    describe('and a .body is set', () => {
      it('should return a number', () => {
        const res = response()

        res.body = null
        assert.strictEqual(res.length, undefined)

        res.body = 'foo'
        res.remove('Content-Length')
        assert.strictEqual(res.length, 3)

        res.body = 'foo'
        assert.strictEqual(res.length, 3)

        res.body = Buffer.from('foo bar')
        res.remove('Content-Length')
        assert.strictEqual(res.length, 7)

        res.body = Buffer.from('foo bar')
        assert.strictEqual(res.length, 7)

        res.body = { hello: 'world' }
        res.remove('Content-Length')
        assert.strictEqual(res.length, 17)

        res.body = { hello: 'world' }
        assert.strictEqual(res.length, 17)

        res.body = fs.createReadStream('package.json')
        assert.strictEqual(res.length, undefined)

        res.body = null
        assert.strictEqual(res.length, undefined)
      })
    })

    describe('and .body is not', () => {
      it('should return undefined', () => {
        const res = response()
        assert.strictEqual(res.length, undefined)
      })
    })
  })

  describe('and a .type is set to json', () => {
    describe('and a .body is set to null', () => {
      it('should return a number', () => {
        const res = response()

        res.type = 'json'
        res.body = null
        assert.strictEqual(res.length, 4)
      })
    })
  })
})

describe('res.length with a web stream body', () => {
  const Koa = require('../..')
  const request = require('supertest')
  const helloStream = () => new ReadableStream({
    start (c) {
      c.enqueue(new TextEncoder().encode('hello world'))
      c.close()
    }
  })

  it('REQ-RES-002 happy: ReadableStream body has no length', () => {
    const res = response()
    res.body = helloStream()
    assert.strictEqual(res.length, undefined)
  })

  it('REQ-RES-002 happy: Response body has no length', () => {
    const res = response()
    res.body = new Response('hello world')
    assert.strictEqual(res.length, undefined)
  })

  it('REQ-RES-002 happy: HEAD sends no Content-Length', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.body = helloStream() })
    const res = await request(app.callback()).head('/')
    assert.strictEqual(res.status, 200)
    assert.strictEqual(res.headers['content-length'], undefined)
  })
})
