'use strict'

const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  APP_NAME: '"Pinecone"',
  NODE_ENV: '"development"',
  API_URL: process.env.API_URL || '"http://127.0.0.1:8000/api/"'
})
