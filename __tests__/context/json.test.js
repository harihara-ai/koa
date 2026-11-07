'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const request = require('supertest')
const Koa = require('../..')
const context = require('../../test-helpers/context')

describe('ctx.json(value)', () => {
  it('REQ-CTX-001 happy: sends an array as JSON', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.json([1, 2]) })
    const res = await request(app.callback()).get('/')
    assert.strictEqual(res.headers['content-type'], 'application/json; charset=utf-8')
    assert.strictEqual(res.text, '[1,2]')
  })

  it('REQ-CTX-001 error: ctx.json(undefined) throws', () => {
    const ctx = context()
    assert.throws(() => ctx.json(undefined),
      { name: 'TypeError', message: 'response.json() needs a JSON value' })
  })
})
