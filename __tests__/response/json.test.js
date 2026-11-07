'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const request = require('supertest')
const Koa = require('../..')
const context = require('../../test-helpers/context')

describe('ctx.response.json(value)', () => {
  it('REQ-RES-001 happy: sends an object as JSON', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.response.json({ a: 1 }) })
    const res = await request(app.callback()).get('/')
    assert.strictEqual(res.status, 200)
    assert.strictEqual(res.headers['content-type'], 'application/json; charset=utf-8')
    assert.strictEqual(res.text, '{"a":1}')
  })

  it('REQ-RES-001 happy: JSON-encodes a string', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.response.json('ok') })
    const res = await request(app.callback()).get('/')
    assert.strictEqual(res.headers['content-type'], 'application/json; charset=utf-8')
    assert.strictEqual(res.text, '"ok"')
  })

  it('REQ-RES-001 error: rejects undefined and leaves the body unchanged', () => {
    const ctx = context()
    ctx.body = 'before'
    assert.throws(() => ctx.response.json(undefined),
      { name: 'TypeError', message: 'response.json() needs a JSON value' })
    assert.strictEqual(ctx.body, 'before')
  })
})
