import React from 'react'
import axios from 'axios'
import Layout from '../components/MyLayout.js'
import Button from 'material-ui/Button'
import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'


const API_BASE_URL = 'https://ycharts.com/api/v3/'


class YCharts extends React.Component {
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
    const res = axios.get(`/api/${this.state.apiReqSubUrl}`)
      .then(response=>{
        console.log(response)
        this.setState({apiResponse: response})
      })
      .catch(console.log)
  }

  render () {
    const { apiReqSubUrl, apiResponse } = this.state
    return (
      <Layout>
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

export default YCharts