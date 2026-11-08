'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const request = require('supertest')
const Koa = require('../..')
const context = require('../../test-helpers/context')

describe('ctx.response.problem(status, detail)', () => {
  it('REQ-RES-002 happy: sends status and detail as problem+json', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.response.problem(404, 'No user 7') })
    const res = await request(app.callback()).get('/')
    assert.strictEqual(res.status, 404)
    assert.strictEqual(res.headers['content-type'], 'application/problem+json')
    assert.strictEqual(res.text, '{"type":"about:blank","title":"Not Found","status":404,"detail":"No user 7"}')
  })

  it('REQ-RES-002 happy: status only leaves out detail', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.response.problem(503) })
    const res = await request(app.callback()).get('/')
    assert.strictEqual(res.status, 503)
    assert.strictEqual(res.text, '{"type":"about:blank","title":"Service Unavailable","status":503}')
  })

  it('REQ-RES-002 error: rejects a status that is not 4xx or 5xx and leaves the body unchanged', () => {
    const ctx = context()
    ctx.body = 'before'
    assert.throws(() => ctx.response.problem(302),
      { name: 'TypeError', message: 'response.problem() needs a 4xx or 5xx status' })
    assert.strictEqual(ctx.body, 'before')
  })

  it('REQ-RES-003 happy: a client that accepts only text/plain gets text', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.response.problem(404, 'No user 7') })
    const res = await request(app.callback()).get('/').set('Accept', 'text/plain')
    assert.strictEqual(res.status, 404)
    assert.strictEqual(res.headers['content-type'], 'text/plain; charset=utf-8')
    assert.strictEqual(res.text, 'Not Found: No user 7')
  })

  it('REQ-RES-003 error: a client that accepts none of the offered types still gets problem+json', async () => {
    const app = new Koa()
    app.use(ctx => { ctx.response.problem(404) })
    const res = await request(app.callback()).get('/').set('Accept', 'image/png')
    assert.strictEqual(res.status, 404)
    assert.strictEqual(res.headers['content-type'], 'application/problem+json')
  })
})
