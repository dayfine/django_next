const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const glob = require('glob')

const entryArray = [
  ...glob.sync('./apps/**/static/**/*.jsx'),
  ...glob.sync('./django_next/static/**/*.jsx'),
]

const entryObject = entryArray.reduce((acc, fp) => {
  const thirdSlash = fp.indexOf('/', 8)
  const fourthSlash = fp.indexOf('/', thirdSlash + 1)
  const lastDot = fp.lastIndexOf('.')
  const name = fp.slice(fourthSlash + 1, lastDot)
  acc[name] = fp
  return acc
}, {})

module.exports = {
  entry: entryObject,
  output: {
    path: path.resolve('./media/'),
    filename: "[name]-[hash].js",
  },
  plugins: [
    new BundleTracker({
      filename: './webpack-stats.json'
    }),
  ],
  optimization: {
    splitChunks: {
      chunks: 'initial',
      cacheGroups: {
        vendor: {
          test: /node_modules\//,
          name: 'vendor',
          priority: 10,
          enforce: true
        },
        commons: {
          test: /common\/|components\//,
          name: 'commons',
          priority: 10,
          enforce: true
        }
      }
    },
    runtimeChunk: {
      name: 'manifest'
    }
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      },
    ],
  },
  resolve: {
    modules: [
      path.resolve('./'),
      'node_modules'
    ],
    extensions: ['.js', '.jsx'],
  },
}
