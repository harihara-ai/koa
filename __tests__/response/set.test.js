'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const context = require('../../test-helpers/context')

describe('ctx.set(name, val)', () => {
  it('should set a field value', () => {
    const ctx = context()
    ctx.set('x-foo', 'bar')
    assert.strictEqual(ctx.response.get('x-foo'), 'bar')
  })

  it('should coerce number to string', () => {
    const ctx = context()
    ctx.set('x-foo', 5)
    assert.strictEqual(ctx.response.header['x-foo'], 5)
  })

  it('should coerce undefined to string', () => {
    const ctx = context()
    ctx.set('x-foo', undefined)
    assert.strictEqual(ctx.response.header['x-foo'], undefined)
  })

  it('should set a field value of array', () => {
    const ctx = context()
    ctx.set('x-foo', ['foo', 'bar', 123])
    assert.deepStrictEqual(ctx.response.header['x-foo'], ['foo', 'bar', 123])
  })
})

describe('ctx.set(object)', () => {
  it('should set multiple fields', () => {
    const ctx = context()

    ctx.set({
      foo: '1',
      bar: '2'
    })

    assert.strictEqual(ctx.response.header.foo, '1')
    assert.strictEqual(ctx.response.header.bar, '2')
  })
})

describe('REQ-RES-001: set an array on a singleton header', () => {
  const refused = name => ({
    name: 'AssertionError',
    message: `Assign multiple ${name} for response header is not allowed`
  })

  it('REQ-RES-001 happy: a single string value is set', () => {
    const ctx = context()
    ctx.set('Location', '/a')
    assert.strictEqual(ctx.response.get('Location'), '/a')
  })

  it('REQ-RES-001 error: an array of two values throws and keeps the value', () => {
    const ctx = context()
    ctx.set('Location', '/old')
    assert.throws(() => ctx.set('Location', ['/a', '/b']), refused('Location'))
    assert.strictEqual(ctx.response.get('Location'), '/old')
  })

  it('REQ-RES-001 edge: a short array throws', () => {
    const ctx = context()
    assert.throws(() => ctx.set('ETag', []), refused('ETag'))
    assert.throws(() => ctx.set('Content-Length', ['5']), refused('Content-Length'))
    assert.strictEqual(ctx.response.get('ETag'), undefined)
    assert.strictEqual(ctx.response.get('Content-Length'), undefined)
  })

  it('REQ-RES-001 edge: a header name in another case throws', () => {
    const ctx = context()
    assert.throws(() => ctx.set('LAST-MODIFIED', ['a', 'b']), refused('Last-Modified'))
  })

  it('REQ-RES-001 edge: other values are set as today', () => {
    const ctx = context()
    ctx.set('Content-Length', 5)
    ctx.set('ETag', '')
    ctx.set('Link', ['<a>', '<b>'])
    assert.strictEqual(ctx.response.get('Content-Length'), 5)
    assert.strictEqual(ctx.response.get('ETag'), '')
    assert.deepStrictEqual(ctx.response.get('Link'), ['<a>', '<b>'])
  })
})
