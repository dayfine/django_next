import Layout from '../components/MyLayout.js'

function Content (props) {
  return (
    <div>
      <h1>{props.url.query.title}</h1>
      <p>This is the blog post content.</p>
    </div>
  )
}

function Post (props) {
  return (
    <Layout>
      <Content url={props.url} />
    </Layout>
  )
}

export default Post
