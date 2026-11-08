'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const request = require('supertest')
const Koa = require('../..')
const context = require('../../test-helpers/context')

describe('ctx.problem(status, detail)', () => {
  it('REQ-CTX-002 happy: ctx.problem sends a problem reply', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.problem(400, 'Bad id') })
    const res = await request(app.callback()).get('/')
    assert.strictEqual(res.status, 400)
    assert.strictEqual(res.headers['content-type'], 'application/problem+json')
    assert.strictEqual(res.text, '{"type":"about:blank","title":"Bad Request","status":400,"detail":"Bad id"}')
  })

  it('REQ-CTX-002 error: ctx.problem(200) throws', () => {
    const ctx = context()
    assert.throws(() => ctx.problem(200),
      { name: 'TypeError', message: 'response.problem() needs a 4xx or 5xx status' })
  })
})
