'use strict'
const process = require('process')
const apiUrl = process.env.API_URL || null

module.exports = {
  APP_NAME: '"Pinecone"',
  NODE_ENV: '"production"',
  API_URL: `"${apiUrl}"`
}
