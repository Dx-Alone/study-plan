// const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '../planner/static'),
  assetsDir: '',
  filenameHashing: false,
  runtimeCompiler: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
};
