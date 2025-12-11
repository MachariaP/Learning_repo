/**
 * Simple GraphQL Server Example
 * 
 * This is a complete working example of a GraphQL server.
 * To run: npm install apollo-server graphql && node simple-server.js
 */

const { ApolloServer, gql } = require('apollo-server');

// Define your GraphQL schema
const typeDefs = gql`
  # User type definition
  type User {
    id: ID!
    name: String!
    email: String!
    age: Int
    posts: [Post!]!
  }

  # Post type definition
  type Post {
    id: ID!
    title: String!
    content: String!
    published: Boolean!
    author: User!
  }

  # Query type - all read operations
  type Query {
    # Get all users
    users: [User!]!
    
    # Get a single user by ID
    user(id: ID!): User
    
    # Get all posts
    posts: [Post!]!
    
    # Get a single post
    post(id: ID!): Post
    
    # Get published posts only
    publishedPosts: [Post!]!
  }

  # Mutation type - all write operations
  type Mutation {
    # Create a new user
    createUser(name: String!, email: String!, age: Int): User!
    
    # Create a new post
    createPost(title: String!, content: String!, authorId: ID!): Post!
    
    # Publish a post
    publishPost(id: ID!): Post!
    
    # Delete a post
    deletePost(id: ID!): DeleteResponse!
  }

  # Response type for deletions
  type DeleteResponse {
    success: Boolean!
    message: String!
  }
`;

// In-memory data store
let users = [
  { id: '1', name: 'Alice Johnson', email: 'alice@example.com', age: 28 },
  { id: '2', name: 'Bob Smith', email: 'bob@example.com', age: 35 },
  { id: '3', name: 'Charlie Brown', email: 'charlie@example.com', age: 42 }
];

let posts = [
  { 
    id: '1', 
    title: 'Introduction to GraphQL', 
    content: 'GraphQL is amazing...', 
    published: true, 
    authorId: '1' 
  },
  { 
    id: '2', 
    title: 'Building APIs with GraphQL', 
    content: 'Learn how to build...', 
    published: true, 
    authorId: '1' 
  },
  { 
    id: '3', 
    title: 'Draft Post', 
    content: 'This is not published yet...', 
    published: false, 
    authorId: '2' 
  }
];

// ID generators
let nextUserId = 4;
let nextPostId = 4;

// Resolver functions
const resolvers = {
  Query: {
    // Get all users
    users: () => users,
    
    // Get single user by ID
    user: (parent, args) => {
      return users.find(user => user.id === args.id);
    },
    
    // Get all posts
    posts: () => posts,
    
    // Get single post by ID
    post: (parent, args) => {
      return posts.find(post => post.id === args.id);
    },
    
    // Get only published posts
    publishedPosts: () => {
      return posts.filter(post => post.published);
    }
  },

  Mutation: {
    // Create a new user
    createUser: (parent, args) => {
      const newUser = {
        id: String(nextUserId++),
        name: args.name,
        email: args.email,
        age: args.age || null
      };
      
      users.push(newUser);
      return newUser;
    },
    
    // Create a new post
    createPost: (parent, args) => {
      // Validate that author exists
      const author = users.find(u => u.id === args.authorId);
      if (!author) {
        throw new Error(`Author with ID ${args.authorId} not found`);
      }
      
      const newPost = {
        id: String(nextPostId++),
        title: args.title,
        content: args.content,
        published: false, // New posts are drafts by default
        authorId: args.authorId
      };
      
      posts.push(newPost);
      return newPost;
    },
    
    // Publish a post
    publishPost: (parent, args) => {
      const post = posts.find(p => p.id === args.id);
      
      if (!post) {
        throw new Error(`Post with ID ${args.id} not found`);
      }
      
      post.published = true;
      return post;
    },
    
    // Delete a post
    deletePost: (parent, args) => {
      const index = posts.findIndex(p => p.id === args.id);
      
      if (index === -1) {
        return {
          success: false,
          message: `Post with ID ${args.id} not found`
        };
      }
      
      posts.splice(index, 1);
      return {
        success: true,
        message: 'Post deleted successfully'
      };
    }
  },

  // Field-level resolvers for User type
  User: {
    // Resolve the posts field for a user
    posts: (parent) => {
      // parent is the User object
      // Find all posts where authorId matches this user's id
      return posts.filter(post => post.authorId === parent.id);
    }
  },

  // Field-level resolvers for Post type
  Post: {
    // Resolve the author field for a post
    author: (parent) => {
      // parent is the Post object
      // Find the user whose id matches this post's authorId
      return users.find(user => user.id === parent.authorId);
    }
  }
};

// Create Apollo Server instance
const server = new ApolloServer({
  typeDefs,
  resolvers,
  // Context function runs for every request
  context: () => ({
    timestamp: new Date().toISOString()
  })
});

// Start the server
server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
  console.log('');
  console.log('Try these queries in the GraphQL Playground:');
  console.log('');
  console.log('1. Get all users with their posts:');
  console.log('   { users { name posts { title } } }');
  console.log('');
  console.log('2. Create a new user:');
  console.log('   mutation { createUser(name: "John", email: "john@example.com") { id name } }');
  console.log('');
  console.log('3. Get published posts with authors:');
  console.log('   { publishedPosts { title author { name } } }');
});
