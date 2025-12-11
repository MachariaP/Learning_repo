/**
 * GraphQL Server with MongoDB Example
 * 
 * This example shows how to connect GraphQL to MongoDB using Mongoose.
 * To run: 
 * 1. Install dependencies: npm install apollo-server graphql mongoose
 * 2. Start MongoDB: sudo systemctl start mongod
 * 3. Run: node mongodb-example.js
 */

const { ApolloServer, gql } = require('apollo-server');
const mongoose = require('mongoose');

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/graphql_example', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
  console.log('✅ Connected to MongoDB');
});

// Define Mongoose Models
const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  age: Number,
  createdAt: { type: Date, default: Date.now }
});

const postSchema = new mongoose.Schema({
  title: { type: String, required: true },
  content: { type: String, required: true },
  published: { type: Boolean, default: false },
  authorId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);
const Post = mongoose.model('Post', postSchema);

// GraphQL Schema
const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    age: Int
    posts: [Post!]!
    createdAt: String!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    published: Boolean!
    author: User!
    createdAt: String!
  }

  type Query {
    # Get all users
    users: [User!]!
    
    # Get a single user by ID
    user(id: ID!): User
    
    # Get all posts
    posts: [Post!]!
    
    # Get published posts only
    publishedPosts: [Post!]!
  }

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

  type DeleteResponse {
    success: Boolean!
    message: String!
  }
`;

// Resolvers
const resolvers = {
  Query: {
    users: async () => {
      return await User.find();
    },
    
    user: async (_, { id }) => {
      return await User.findById(id);
    },
    
    posts: async () => {
      return await Post.find();
    },
    
    publishedPosts: async () => {
      return await Post.find({ published: true });
    }
  },

  Mutation: {
    createUser: async (_, { name, email, age }) => {
      const user = new User({ name, email, age });
      return await user.save();
    },
    
    createPost: async (_, { title, content, authorId }) => {
      // Validate author exists
      const author = await User.findById(authorId);
      if (!author) {
        throw new Error('Author not found');
      }
      
      const post = new Post({ title, content, authorId });
      return await post.save();
    },
    
    publishPost: async (_, { id }) => {
      const post = await Post.findById(id);
      if (!post) {
        throw new Error('Post not found');
      }
      
      post.published = true;
      return await post.save();
    },
    
    deletePost: async (_, { id }) => {
      const result = await Post.findByIdAndDelete(id);
      
      if (!result) {
        return {
          success: false,
          message: 'Post not found'
        };
      }
      
      return {
        success: true,
        message: 'Post deleted successfully'
      };
    }
  },

  // Field resolvers
  User: {
    // Resolve posts for a user
    posts: async (parent) => {
      return await Post.find({ authorId: parent._id });
    }
  },

  Post: {
    // Resolve author for a post
    author: async (parent) => {
      return await User.findById(parent.authorId);
    }
  }
};

// Create Apollo Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: () => ({
    models: { User, Post }
  })
});

// Start server
server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
  console.log('');
  console.log('Try these example queries:');
  console.log('');
  console.log('1. Create a user:');
  console.log('   mutation { createUser(name: "Alice", email: "alice@example.com", age: 25) { id name } }');
  console.log('');
  console.log('2. Create a post:');
  console.log('   mutation { createPost(title: "My Post", content: "Content here", authorId: "USER_ID") { id title } }');
  console.log('');
  console.log('3. Get users with posts:');
  console.log('   { users { name posts { title } } }');
});
