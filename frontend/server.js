const express = require('express')
const axios = require('axios');
const bodyParser = require('body-parser')
const fetch = require('isomorphic-unfetch')
const morgan = require('morgan')
const cors = require('cors')
const next = require('next')

require('dotenv').config()
const API_KEY = process.env.YC_API_KEY
const dev = process.env.NODE_ENV !== 'production'
const app = next({ dev })
const handle = app.getRequestHandler()


app
  .prepare()
  .then(() => {
    const server = express()

    server.use(bodyParser.urlencoded({ extended: false }))
    server.use(bodyParser.json())
    server.use(morgan('dev'))
    server.use(cors())

    server.get('/p/:id', (req, res) => {
      const actualPage = '/post'
      const queryParams = { id: req.params.id }
      app.render(req, res, actualPage, queryParams)
    })

    server.get('/t/:id', (req, res) => {
      const actualPage = '/pet'
      const queryParams = { id: req.params.id }
      app.render(req, res, actualPage, queryParams)
    })

    server.get('/api/*', (req, res, next)=> {
      const API_BASE_URL = 'https://ycharts.com/api/v3/'
      const apiReqSubUrl = req.originalUrl.slice(5)
      console.log(`${API_BASE_URL}${apiReqSubUrl}`, API_KEY)
      fetch(`${API_BASE_URL}${apiReqSubUrl}`, {
          headers: {
            'X-YCHARTSAUTHORIZATION': API_KEY,
          }
        })
        .then(response=>{
          console.log(Object.keys(response))
          res.send({
            //full: response,
            results: response.response,
            // status: response.status,
          })
        })
        .catch(next)
    })

    server.get('*', (req, res) => {
      return handle(req, res)
    })

    server.listen(3000, (err) => {
      if (err) throw err
      console.log('> Ready on http://localhost:3000')
    })

  })
  .catch(ex => {
    console.error(ex.stack)
    process.exit(1)
  })
