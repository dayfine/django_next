const withCSS = require('@zeit/next-css')
const commonsChunkConfig = require('@zeit/next-css/commons-chunk-config')

module.exports = withCSS({
  exportPathMap() {
    return {
      '/': { page: '/' },
      '/about': { page: '/about' },
      '/p/hello-nextjs': { page: '/post', query: { title: 'Hello Next.js' } },
      '/p/learn-nextjs': { page: '/post', query: { title: 'Learn Next.js is awesome' } },
      '/p/deploy-nextjs': { page: '/post', query: { title: 'Deploy apps with Zeit' } },
      '/p/exporting-pages': { page: '/post', query: { title: 'Learn to Export HTML Pages' } }
    }
  },
  webpack(config) {
    config = commonsChunkConfig(config, /\.(sass|scss|css)$/);
    return config
  }
})
