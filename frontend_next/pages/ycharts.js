import React from 'react'
import axios from 'axios'
import Layout from '../components/MyLayout.js'
import Button from 'material-ui/Button'
import TextField from 'material-ui/TextField'



const API_BASE_URL = 'https://ycharts.com/api/v3'


class YCharts extends React.Component {
  state = {
    apiRequestUrl: API_BASE_URL
  }

  handleChange = name => evt => {
    this.setState({[name]: evt.target.value})
  }

  handleAPIRequest = () => {

  }

  render () {
    return (
      <Layout>
        <TextField
          label='API request url'
          value={this.state.apiRequestUrl}
          onChange={this.handleChange('apiRequestUrl')}
        />
        <Button onClick={this.handleAPIRequest()}>Click me</Button>
      </Layout>
    )
  }
}

export default YCharts