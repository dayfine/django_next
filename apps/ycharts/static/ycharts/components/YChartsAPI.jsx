import React from 'react'
import ReactDOM from 'react-dom'
import Button from 'material-ui/Button'
import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'

import Layout from 'django_next/static/components/common/Layout'


const API_BASE_URL = 'https://ycharts.com/api/v3/'


class YChartsAPI extends React.Component {
  state = {
    apiReqSubUrl: '',
    apiResponse: 'Nothing Yet'
  }

  handleChange = name => evt => {
    if (name==='apiReqSubUrl') {
      const subUrl = evt.target.value.slice(API_BASE_URL.length)
      this.setState({[name]: subUrl})
    }
  }

  handleAPIRequest = () => {
    console.log('soon enough')
  }

  render () {
    const { apiReqSubUrl, apiResponse } = this.state
    return (
      <Layout col={5}>
        <div className='center col-xs-10'>
          <div className='row'>
            <TextField
              label='API request url'
              value={`${API_BASE_URL}${apiReqSubUrl}`}
              onChange={this.handleChange('apiReqSubUrl')}
              fullWidth
            />
          </div>
          <div className='row'>
            <Button
              onClick={this.handleAPIRequest}
              variant='raised'>
              Send API Request
            </Button>

          </div>
          <Paper>
            <pre>{JSON.stringify(apiResponse)}</pre>
          </Paper>
        </div>
      </Layout>
    )
  }
}


ReactDOM.render(
  React.createElement(YChartsAPI, window.props),
  window.react_mount,
)
