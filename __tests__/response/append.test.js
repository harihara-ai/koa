'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const context = require('../../test-helpers/context')

describe('ctx.append(name, val)', () => {
  it('should append multiple headers', () => {
    const ctx = context()
    ctx.append('x-foo', 'bar1')
    ctx.append('x-foo', 'bar2')
    assert.deepStrictEqual(ctx.response.header['x-foo'], ['bar1', 'bar2'])
  })

  it('should accept array of values', () => {
    const ctx = context()

    ctx.append('Set-Cookie', ['foo=bar', 'fizz=buzz'])
    ctx.append('Set-Cookie', 'hi=again')
    assert.deepStrictEqual(ctx.response.header['set-cookie'], ['foo=bar', 'fizz=buzz', 'hi=again'])
  })

  it('should get reset by res.set(field, val)', () => {
    const ctx = context()

    ctx.append('Link', '<http://localhost/>')
    ctx.append('Link', '<http://localhost:80/>')

    ctx.set('Link', '<http://127.0.0.1/>')

    assert.strictEqual(ctx.response.header.link, '<http://127.0.0.1/>')
  })

  it('should work with res.set(field, val) first', () => {
    const ctx = context()

    ctx.set('Link', '<http://localhost/>')
    ctx.append('Link', '<http://localhost:80/>')

    assert.deepStrictEqual(ctx.response.header.link, ['<http://localhost/>', '<http://localhost:80/>'])
  })
})

describe('REQ-RES-003: append to a singleton header', () => {
  it('REQ-RES-003 happy: the first append sets the value', () => {
    const ctx = context()
    ctx.append('Location', '/a')
    assert.strictEqual(ctx.response.get('Location'), '/a')
  })

  it('REQ-RES-003 error: a second append throws and keeps the value', () => {
    const ctx = context()
    ctx.append('Location', '/a')
    assert.throws(() => ctx.append('Location', '/b'), {
      name: 'AssertionError',
      message: 'Assign multiple Location for response header is not allowed'
    })
    assert.strictEqual(ctx.response.get('Location'), '/a')
  })
})
