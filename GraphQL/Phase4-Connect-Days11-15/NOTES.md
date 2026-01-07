# Phase 4: Connect to Databases and Add Authentication (Days 11-15)

## Learning Objectives
By the end of this phase, you should:
- Connect GraphQL servers to real databases (MongoDB, PostgreSQL)
- Implement authentication and authorization
- Use DataLoader to solve the N+1 problem
- Handle database relationships efficiently
- Implement JWT-based authentication
- Protect routes with authentication middleware

---

## Day 11-12: Database Integration

### Why Use a Real Database?

In-memory data:
- ❌ Lost when server restarts
- ❌ Doesn't scale
- ❌ No persistence

Real database:
- ✅ Persistent storage
- ✅ Scalable
- ✅ ACID transactions
- ✅ Production-ready

### Option 1: MongoDB (NoSQL)

**Best for:** Flexible schemas, rapid prototyping, JSON-like data

**Setup:**
```bash
# Install dependencies
npm install mongoose

# Or use MongoDB Atlas (cloud) - no local installation needed
```

**Connection:**
```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/graphql-blog', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'Connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});
```

**Define Models:**
```javascript
// models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', userSchema);
```

```javascript
// models/Post.js
const mongoose = require('mongoose');

const postSchema = new mongoose.Schema({
  title: { type: String, required: true },
  content: { type: String, required: true },
  published: { type: Boolean, default: false },
  authorId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Post', postSchema);
```

**Update Resolvers:**
```javascript
const User = require('./models/User');
const Post = require('./models/Post');

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
    }
  },

  Mutation: {
    createUser: async (_, { name, email, password }) => {
      const user = new User({ name, email, password });
      return await user.save();
    },
    
    createPost: async (_, { title, content, authorId }) => {
      const post = new Post({ title, content, authorId });
      return await post.save();
    }
  },

  User: {
    posts: async (parent) => {
      return await Post.find({ authorId: parent._id });
    }
  },

  Post: {
    author: async (parent) => {
      return await User.findById(parent.authorId);
    }
  }
};
```

### Option 2: PostgreSQL (SQL)

**Best for:** Structured data, complex relationships, ACID compliance

**Setup:**
```bash
# Install dependencies
npm install pg
# Or use Prisma for easier integration
npm install @prisma/client
npx prisma init
```

**Using pg (PostgreSQL driver):**
```javascript
const { Pool } = require('pg');

const pool = new Pool({
  user: 'your_user',
  host: 'localhost',
  database: 'graphql_db',
  password: 'your_password',
  port: 5432,
});

// Query example
const resolvers = {
  Query: {
    users: async () => {
      const result = await pool.query('SELECT * FROM users');
      return result.rows;
    },
    
    user: async (_, { id }) => {
      const result = await pool.query(
        'SELECT * FROM users WHERE id = $1',
        [id]
      );
      return result.rows[0];
    }
  },

  Mutation: {
    createUser: async (_, { name, email }) => {
      const result = await pool.query(
        'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
        [name, email]
      );
      return result.rows[0];
    }
  }
};
```

**Using Prisma (Recommended for PostgreSQL):**

1. Define schema (schema.prisma):
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
}
```

2. Generate Prisma client:
```bash
npx prisma generate
npx prisma migrate dev --name init
```

3. Use in resolvers:
```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const resolvers = {
  Query: {
    users: async () => {
      return await prisma.user.findMany();
    },
    
    user: async (_, { id }) => {
      return await prisma.user.findUnique({
        where: { id: parseInt(id) }
      });
    }
  },

  Mutation: {
    createUser: async (_, { name, email }) => {
      return await prisma.user.create({
        data: { name, email }
      });
    }
  },

  User: {
    posts: async (parent) => {
      return await prisma.post.findMany({
        where: { authorId: parent.id }
      });
    }
  }
};
```

---

## Day 13: Authentication

### JWT-Based Authentication

**Install Dependencies:**
```bash
npm install jsonwebtoken bcrypt
```

**Password Hashing:**
```javascript
const bcrypt = require('bcrypt');

// Hash password before saving
const hashPassword = async (password) => {
  return await bcrypt.hash(password, 10);
};

// Compare passwords
const comparePasswords = async (password, hashedPassword) => {
  return await bcrypt.compare(password, hashedPassword);
};
```

**Generate JWT Tokens:**
```javascript
const jwt = require('jsonwebtoken');

const SECRET_KEY = 'your-secret-key'; // Use environment variable in production

// Create token
const createToken = (user) => {
  return jwt.sign(
    { 
      userId: user.id,
      email: user.email 
    },
    SECRET_KEY,
    { expiresIn: '7d' }
  );
};

// Verify token
const verifyToken = (token) => {
  try {
    return jwt.verify(token, SECRET_KEY);
  } catch (error) {
    throw new Error('Invalid token');
  }
};
```

**Update Schema:**
```graphql
type AuthPayload {
  token: String!
  user: User!
}

type Mutation {
  signup(name: String!, email: String!, password: String!): AuthPayload!
  login(email: String!, password: String!): AuthPayload!
}
```

**Auth Resolvers:**
```javascript
const resolvers = {
  Mutation: {
    signup: async (_, { name, email, password }) => {
      // Check if user exists
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        throw new Error('User already exists');
      }

      // Hash password
      const hashedPassword = await hashPassword(password);

      // Create user
      const user = new User({
        name,
        email,
        password: hashedPassword
      });
      await user.save();

      // Generate token
      const token = createToken(user);

      return {
        token,
        user
      };
    },

    login: async (_, { email, password }) => {
      // Find user
      const user = await User.findOne({ email });
      if (!user) {
        throw new Error('Invalid credentials');
      }

      // Verify password
      const validPassword = await comparePasswords(password, user.password);
      if (!validPassword) {
        throw new Error('Invalid credentials');
      }

      // Generate token
      const token = createToken(user);

      return {
        token,
        user
      };
    }
  }
};
```

**Add Authentication to Context:**
```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    // Get token from header
    const token = req.headers.authorization || '';
    
    // Extract token (format: "Bearer <token>")
    const actualToken = token.replace('Bearer ', '');
    
    // Verify and decode token
    let user = null;
    if (actualToken) {
      try {
        const decoded = verifyToken(actualToken);
        user = decoded;
      } catch (error) {
        // Invalid token - user remains null
      }
    }

    return {
      user,
      prisma // or mongoose models
    };
  }
});
```

**Protect Resolvers:**
```javascript
const requireAuth = (user) => {
  if (!user) {
    throw new Error('Not authenticated');
  }
};

const resolvers = {
  Query: {
    me: (_, __, { user }) => {
      requireAuth(user);
      return User.findById(user.userId);
    }
  },

  Mutation: {
    createPost: async (_, { title, content }, { user }) => {
      requireAuth(user);
      
      const post = new Post({
        title,
        content,
        authorId: user.userId
      });
      
      return await post.save();
    },

    deletePost: async (_, { id }, { user }) => {
      requireAuth(user);
      
      const post = await Post.findById(id);
      
      // Check ownership
      if (post.authorId.toString() !== user.userId) {
        throw new Error('Not authorized');
      }
      
      await post.remove();
      return { success: true, message: 'Post deleted' };
    }
  }
};
```

---

## Day 14-15: Performance Optimization with DataLoader

### The N+1 Problem

**Problem:** Fetching related data causes N+1 database queries.

```graphql
query {
  users {        # 1 query - get all users
    name
    posts {      # N queries - one per user!
      title
    }
  }
}
```

If you have 100 users, this makes 101 queries! ❌

### DataLoader Solution

DataLoader batches and caches requests automatically.

**Install:**
```bash
npm install dataloader
```

**Create Data Loaders:**
```javascript
const DataLoader = require('dataloader');

// Batch function: receives array of IDs, returns array of results
const createPostsByUserIdLoader = () => {
  return new DataLoader(async (userIds) => {
    // Fetch all posts for all userIds in one query
    const posts = await Post.find({
      authorId: { $in: userIds }
    });

    // Group posts by userId
    const postsByUserId = {};
    posts.forEach(post => {
      if (!postsByUserId[post.authorId]) {
        postsByUserId[post.authorId] = [];
      }
      postsByUserId[post.authorId].push(post);
    });

    // Return posts in same order as userIds
    return userIds.map(userId => postsByUserId[userId] || []);
  });
};

const createUserByIdLoader = () => {
  return new DataLoader(async (userIds) => {
    const users = await User.find({
      _id: { $in: userIds }
    });

    // Create a map for O(1) lookup
    const userMap = {};
    users.forEach(user => {
      userMap[user._id.toString()] = user;
    });

    // Return users in same order as userIds
    return userIds.map(id => userMap[id.toString()]);
  });
};
```

**Add Loaders to Context:**
```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    return {
      user: getUserFromToken(req),
      loaders: {
        postsByUserId: createPostsByUserIdLoader(),
        userById: createUserByIdLoader()
      }
    };
  }
});
```

**Use in Resolvers:**
```javascript
const resolvers = {
  User: {
    posts: async (parent, _, { loaders }) => {
      // Batched and cached automatically!
      return await loaders.postsByUserId.load(parent._id.toString());
    }
  },

  Post: {
    author: async (parent, _, { loaders }) => {
      // Batched and cached automatically!
      return await loaders.userById.load(parent.authorId.toString());
    }
  }
};
```

**Result:** 100 users → 2 queries instead of 101! ✅

### DataLoader Benefits

1. **Batching**: Multiple `load()` calls in single request → one database query
2. **Caching**: Same ID loaded multiple times → returns cached result
3. **Automatic**: Works without changing query/mutation code

---

## Complete Example: Authenticated API with Database

```javascript
const { ApolloServer, gql } = require('apollo-server');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const DataLoader = require('dataloader');

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/graphql-auth-api');

// Models
const User = require('./models/User');
const Post = require('./models/Post');

// Schema
const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    published: Boolean!
    author: User!
  }

  type AuthPayload {
    token: String!
    user: User!
  }

  type Query {
    me: User
    users: [User!]!
    posts: [Post!]!
  }

  type Mutation {
    signup(name: String!, email: String!, password: String!): AuthPayload!
    login(email: String!, password: String!): AuthPayload!
    createPost(title: String!, content: String!): Post!
  }
`;

// Helper functions
const createToken = (user) => {
  return jwt.sign(
    { userId: user._id, email: user.email },
    'SECRET_KEY',
    { expiresIn: '7d' }
  );
};

const requireAuth = (user) => {
  if (!user) throw new Error('Not authenticated');
};

// DataLoaders
const createLoaders = () => ({
  postsByUserId: new DataLoader(async (userIds) => {
    const posts = await Post.find({ authorId: { $in: userIds } });
    const grouped = {};
    posts.forEach(post => {
      if (!grouped[post.authorId]) grouped[post.authorId] = [];
      grouped[post.authorId].push(post);
    });
    return userIds.map(id => grouped[id] || []);
  }),

  userById: new DataLoader(async (ids) => {
    const users = await User.find({ _id: { $in: ids } });
    const map = {};
    users.forEach(user => { map[user._id] = user; });
    return ids.map(id => map[id]);
  })
});

// Resolvers
const resolvers = {
  Query: {
    me: async (_, __, { user }) => {
      requireAuth(user);
      return await User.findById(user.userId);
    },
    users: async () => await User.find(),
    posts: async () => await Post.find()
  },

  Mutation: {
    signup: async (_, { name, email, password }) => {
      const hashedPassword = await bcrypt.hash(password, 10);
      const user = new User({ name, email, password: hashedPassword });
      await user.save();
      const token = createToken(user);
      return { token, user };
    },

    login: async (_, { email, password }) => {
      const user = await User.findOne({ email });
      if (!user) throw new Error('Invalid credentials');
      
      const valid = await bcrypt.compare(password, user.password);
      if (!valid) throw new Error('Invalid credentials');
      
      const token = createToken(user);
      return { token, user };
    },

    createPost: async (_, { title, content }, { user }) => {
      requireAuth(user);
      const post = new Post({ title, content, authorId: user.userId });
      return await post.save();
    }
  },

  User: {
    posts: async (parent, _, { loaders }) => {
      return await loaders.postsByUserId.load(parent._id.toString());
    }
  },

  Post: {
    author: async (parent, _, { loaders }) => {
      return await loaders.userById.load(parent.authorId.toString());
    }
  }
};

// Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    let user = null;
    
    if (token) {
      try {
        user = jwt.verify(token, 'SECRET_KEY');
      } catch (e) {}
    }

    return {
      user,
      loaders: createLoaders()
    };
  }
});

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
```

---

## Checklist: What You Should Know

After completing Phase 4, you should be able to:

- [ ] Connect GraphQL to MongoDB
- [ ] Connect GraphQL to PostgreSQL
- [ ] Define database models/schemas
- [ ] Implement user authentication
- [ ] Hash passwords securely
- [ ] Generate and verify JWT tokens
- [ ] Protect resolvers with authentication
- [ ] Use DataLoader to solve N+1 problems
- [ ] Implement authorization (ownership checks)
- [ ] Structure production-ready GraphQL projects

---

## Next Steps

Ready for Phase 5?
- Build React frontend with Apollo Client
- Deploy your API to production
- Add logging and monitoring
- Implement advanced features

**Great work!** You now have a production-ready GraphQL backend!
