const { startDevServer } = require('@cypress/webpack-dev-server')
// const webpackConfig = require('@vue/cli-service/webpack.config.js')
const { isFileExist } = require('cy-verify-downloads');

module.exports = (on, config) => {
  on('dev-server:start', options =>
    startDevServer({
      options
    })
  )
  return config
}
module.exports = (on, config) => {
  on('task', { isFileExist })
  return config
}