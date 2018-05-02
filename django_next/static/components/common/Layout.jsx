import React from 'react'
import Grid from 'material-ui/Grid'

function Layout(props) {
  return (
    <Grid container>
      <Grid item xs={props.col}>
        {props.children}
      </Grid>
    </Grid>
  )
}

export default Layout