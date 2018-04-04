import Layout from '../components/MyLayout.js'
import Link from 'next/link'

function PostLink (props) {
  return (
    <li>
      <Link as={`/t/${props.id}`} href={`/pet?title=${props.title}`}>
        <a>{props.title}</a>
      </Link>
    </li>
  )
}

function Index () {
  return (
    <Layout>
      <h1>My Blog</h1>
      <ul>
        <PostLink id='hello-nextjs' title='Hello Next.js' />
        <PostLink id='learn-nextjs' title='Learn Next.js is awesome' />
        <PostLink id='deploy-nextjs' title='Deploy apps with Zeit' />
      </ul>
    </Layout>
  )
}

export default Index
