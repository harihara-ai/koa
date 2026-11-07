module.exports = (obj, keys) => Object.fromEntries(
  keys.map((key) => [key, obj[key]]).filter(([, value]) => value != null)
)
