'use strict'

const { describe, it } = require('node:test')
const assert = require('node:assert/strict')
const only = require('../../lib/only.js')

describe('only(obj, keys)', () => {
  it('CHAR: keeps the listed keys in key order', () => {
    const out = only({ a: 1, b: 2, c: 3 }, ['c', 'a'])
    assert.deepStrictEqual(Object.keys(out), ['c', 'a'])
    assert.deepStrictEqual(out, { c: 3, a: 1 })
  })

  it('CHAR: drops null and undefined, keeps 0, false and empty string', () => {
    const out = only({ n: null, u: undefined, z: 0, f: false, s: '' }, ['n', 'u', 'z', 'f', 's', 'missing'])
    assert.deepStrictEqual(out, { z: 0, f: false, s: '' })
  })

  it('CHAR: reads getters and inherited values', () => {
    const proto = { get g () { return 'got' }, inherited: 'base' }
    const obj = Object.create(proto)
    obj.own = 'mine'
    assert.deepStrictEqual(only(obj, ['own', 'g', 'inherited']), { own: 'mine', g: 'got', inherited: 'base' })
  })
})
