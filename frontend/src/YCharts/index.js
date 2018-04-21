import React from 'react'
import axios from 'axios'
import Button from 'material-ui/Button'
import Paper from 'material-ui/Paper'
import TextField from 'material-ui/TextField'


const API_BASE_URL = 'https://ycharts.com/api/v3'


class YCharts extends React.Component {
  state = {
    apiRequestUrl: API_BASE_URL,
    APIResponse: 'Nothing Yet'
  }

  handleChange = name => evt => {
    this.setState({[name]: evt.target.value})
  }

  handleAPIRequest = () => {

  }

  render () {
    return (
      <div className='container'>
        <div className='center col-xs-10'>
          <div className='row'>
            <TextField
              label='API request url'
              value={this.state.apiRequestUrl}
              onChange={this.handleChange('apiRequestUrl')}
              fullWidth
            />
          </div>
          <div className='row'>
            <Button
              onClick={this.handleAPIRequest()}
              variant='raised'>
              Send API Request
            </Button>

          </div>
          <Paper>
            <pre>{this.state.APIResponse}</pre>
          </Paper>
        </div>
      </div>
    )
  }
}

export default YCharts