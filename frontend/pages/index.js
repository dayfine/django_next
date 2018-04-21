import Layout from '../components/MyLayout.js'
import Link from 'next/link'
import withRoot from '../src/withRoot'

function PostLink ({ post }) {
  return (
    <li>
      <Link as={`/t/${post.id}`} href={`/pet?title=${post.title}`}>
        <a>{post.title}</a>
      </Link>
      <style jsx>{`
        li {
          list-style: none;
          margin: 5px 0;
        }
        a {
          font-family: "Arial";
          text-decoration: none;
          color: blue;
        }
        a:hover {
          opacity: 0.6;
        }
    `}</style>
    </li>
  )
}

function getPosts() {
  return [
    { id: 'hello-nextjs', title: 'Hello Next.js'},
    { id: 'learn-nextjs', title: 'Learn Next.js is awesome'},
    { id: 'deploy-nextjs', title: 'Deploy apps with ZEIT'},
  ]
}

function Index () {
  return (
    <Layout>
      <h1>My Blog</h1>
      <ul>
        {getPosts().map(post => (
          <PostLink key={post.id} post={post} />
        ))}
      </ul>
      <style jsx>{`
        h1 {
          font-family: "Arial";
        }
        ul {
          padding: 0;
        }
    `}</style>
    </Layout>
  )
}

export default withRoot(Index)
