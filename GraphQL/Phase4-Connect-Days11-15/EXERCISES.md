# Phase 4: Terminal Exercises (Days 11-15)

Practice database integration and authentication in your terminal.

---

## Exercise 1: Setup MongoDB Locally

**Goal**: Install and configure MongoDB for local development.

### Install MongoDB (Ubuntu/Debian)
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Create list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update package database
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify installation
mongod --version

# Check status
sudo systemctl status mongod
```

### Using MongoDB Shell
```bash
# Connect to MongoDB
mongosh

# Show databases
show dbs

# Create/use database
use graphql_blog

# Create a collection and insert data
db.users.insertOne({
  name: "Alice",
  email: "alice@example.com",
  createdAt: new Date()
})

# Query data
db.users.find()

# Exit
exit
```

**Tasks**:
1. Install MongoDB on your system
2. Create a database called `graphql_learning`
3. Insert 5 test users
4. Query and filter the users

---

## Exercise 2: Create MongoDB-Backed GraphQL API

**Goal**: Build a GraphQL server with MongoDB persistence.

### Step 1: Setup Project
```bash
mkdir graphql-mongodb-api && cd graphql-mongodb-api
npm init -y
npm install apollo-server graphql mongoose
```

### Step 2: Create Models
```bash
mkdir models

cat > models/User.js << 'EOF'
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  age: Number,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', userSchema);
EOF

cat > models/Post.js << 'EOF'
const mongoose = require('mongoose');

const postSchema = new mongoose.Schema({
  title: { type: String, required: true },
  content: { type: String, required: true },
  published: { type: Boolean, default: false },
  authorId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Post', postSchema);
EOF
```

### Step 3: Create Server
```bash
cat > server.js << 'EOF'
const { ApolloServer, gql } = require('apollo-server');
const mongoose = require('mongoose');
const User = require('./models/User');
const Post = require('./models/Post');

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/graphql_learning');

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    age: Int
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    published: Boolean!
    author: User!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
    posts: [Post!]!
  }

  type Mutation {
    createUser(name: String!, email: String!, age: Int): User!
    createPost(title: String!, content: String!, authorId: ID!): Post!
    publishPost(id: ID!): Post!
  }
`;

const resolvers = {
  Query: {
    users: async () => await User.find(),
    user: async (_, { id }) => await User.findById(id),
    posts: async () => await Post.find()
  },

  Mutation: {
    createUser: async (_, args) => {
      const user = new User(args);
      return await user.save();
    },

    createPost: async (_, { title, content, authorId }) => {
      const post = new Post({ title, content, authorId });
      return await post.save();
    },

    publishPost: async (_, { id }) => {
      const post = await Post.findById(id);
      post.published = true;
      return await post.save();
    }
  },

  User: {
    posts: async (parent) => await Post.find({ authorId: parent._id })
  },

  Post: {
    author: async (parent) => await User.findById(parent.authorId)
  }
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
  console.log(`🚀 Server with MongoDB ready at ${url}`);
});
EOF
```

### Step 4: Test the API
```bash
# Start server
node server.js &
SERVER_PID=$!
sleep 3

# Create a user
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(name: \"John Doe\", email: \"john@example.com\", age: 30) { id name } }"}' | jq '.'

# Get all users
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name email } }"}' | jq '.'

# Stop server
kill $SERVER_PID
```

**Tasks**:
1. Add a delete user mutation
2. Add pagination to the users query
3. Add search functionality
4. Add update user mutation

---

## Exercise 3: Implement Authentication

**Goal**: Add JWT-based authentication to your API.

### Step 1: Install Dependencies
```bash
npm install jsonwebtoken bcrypt
```

### Step 2: Update User Model
```bash
cat > models/User.js << 'EOF'
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', userSchema);
EOF
```

### Step 3: Create Auth Utils
```bash
cat > auth.js << 'EOF'
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const SECRET_KEY = 'your-secret-key-change-in-production';

const hashPassword = async (password) => {
  return await bcrypt.hash(password, 10);
};

const comparePasswords = async (password, hashedPassword) => {
  return await bcrypt.compare(password, hashedPassword);
};

const createToken = (user) => {
  return jwt.sign(
    { userId: user._id, email: user.email },
    SECRET_KEY,
    { expiresIn: '7d' }
  );
};

const verifyToken = (token) => {
  try {
    return jwt.verify(token, SECRET_KEY);
  } catch (error) {
    return null;
  }
};

module.exports = {
  hashPassword,
  comparePasswords,
  createToken,
  verifyToken
};
EOF
```

### Step 4: Create Auth Server
```bash
cat > auth-server.js << 'EOF'
const { ApolloServer, gql } = require('apollo-server');
const mongoose = require('mongoose');
const User = require('./models/User');
const { hashPassword, comparePasswords, createToken, verifyToken } = require('./auth');

mongoose.connect('mongodb://localhost:27017/graphql_auth');

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type AuthPayload {
    token: String!
    user: User!
  }

  type Query {
    me: User
  }

  type Mutation {
    signup(name: String!, email: String!, password: String!): AuthPayload!
    login(email: String!, password: String!): AuthPayload!
  }
`;

const resolvers = {
  Query: {
    me: async (_, __, { user }) => {
      if (!user) throw new Error('Not authenticated');
      return await User.findById(user.userId);
    }
  },

  Mutation: {
    signup: async (_, { name, email, password }) => {
      const existing = await User.findOne({ email });
      if (existing) throw new Error('User already exists');

      const hashedPassword = await hashPassword(password);
      const user = new User({ name, email, password: hashedPassword });
      await user.save();

      const token = createToken(user);
      return { token, user };
    },

    login: async (_, { email, password }) => {
      const user = await User.findOne({ email });
      if (!user) throw new Error('Invalid credentials');

      const valid = await comparePasswords(password, user.password);
      if (!valid) throw new Error('Invalid credentials');

      const token = createToken(user);
      return { token, user };
    }
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    const token = req.headers.authorization?.replace('Bearer ', '') || '';
    const user = verifyToken(token);
    return { user };
  }
});

server.listen().then(({ url }) => {
  console.log(`🚀 Auth server ready at ${url}`);
});
EOF
```

### Step 5: Test Authentication
```bash
# Start server
node auth-server.js &
SERVER_PID=$!
sleep 3

# Signup
RESPONSE=$(curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { signup(name: \"Alice\", email: \"alice@test.com\", password: \"password123\") { token user { id name email } } }"}')

echo "Signup response:"
echo "$RESPONSE" | jq '.'

# Extract token
TOKEN=$(echo "$RESPONSE" | jq -r '.data.signup.token')

echo ""
echo "Token: $TOKEN"

# Test protected route with token
echo ""
echo "Testing protected route:"
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "{ me { id name email } }"}' | jq '.'

# Test without token (should fail)
echo ""
echo "Testing without token (should fail):"
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ me { id name email } }"}' | jq '.'

# Login
echo ""
echo "Testing login:"
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { login(email: \"alice@test.com\", password: \"password123\") { token user { name } } }"}' | jq '.'

# Stop server
kill $SERVER_PID
```

**Tasks**:
1. Add password reset functionality
2. Add email verification
3. Add refresh tokens
4. Add role-based authorization

---

## Exercise 4: Implement DataLoader

**Goal**: Optimize N+1 queries with DataLoader.

### Setup
```bash
npm install dataloader
```

### Create DataLoader Example
```bash
cat > dataloader-server.js << 'EOF'
const { ApolloServer, gql } = require('apollo-server');
const mongoose = require('mongoose');
const DataLoader = require('dataloader');
const User = require('./models/User');
const Post = require('./models/Post');

mongoose.connect('mongodb://localhost:27017/graphql_dataloader');

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
    author: User!
  }

  type Query {
    users: [User!]!
    posts: [Post!]!
  }
`;

// Create loaders
const createLoaders = () => {
  const postsByUserIdLoader = new DataLoader(async (userIds) => {
    console.log('Batch loading posts for users:', userIds);
    
    const posts = await Post.find({
      authorId: { $in: userIds }
    });

    const postsByUserId = {};
    posts.forEach(post => {
      const uid = post.authorId.toString();
      if (!postsByUserId[uid]) postsByUserId[uid] = [];
      postsByUserId[uid].push(post);
    });

    return userIds.map(id => postsByUserId[id.toString()] || []);
  });

  const userByIdLoader = new DataLoader(async (userIds) => {
    console.log('Batch loading users:', userIds);
    
    const users = await User.find({
      _id: { $in: userIds }
    });

    const userMap = {};
    users.forEach(user => {
      userMap[user._id.toString()] = user;
    });

    return userIds.map(id => userMap[id.toString()]);
  });

  return {
    postsByUserIdLoader,
    userByIdLoader
  };
};

const resolvers = {
  Query: {
    users: async () => await User.find(),
    posts: async () => await Post.find()
  },

  User: {
    posts: async (parent, _, { loaders }) => {
      return await loaders.postsByUserIdLoader.load(parent._id.toString());
    }
  },

  Post: {
    author: async (parent, _, { loaders }) => {
      return await loaders.userByIdLoader.load(parent.authorId.toString());
    }
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: () => ({
    loaders: createLoaders()
  })
});

server.listen().then(({ url }) => {
  console.log(`🚀 DataLoader server ready at ${url}`);
  console.log('Watch the console for batch loading logs!');
});
EOF
```

### Test DataLoader
```bash
# Start server
node dataloader-server.js &
SERVER_PID=$!
sleep 3

# Create test data first
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(name: \"User1\", email: \"u1@test.com\") { id } }"}' > /dev/null

curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(name: \"User2\", email: \"u2@test.com\") { id } }"}' > /dev/null

# Query that would normally cause N+1
echo "Testing N+1 query (watch server logs):"
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { name posts { title } } }"}' | jq '.'

# Stop server
kill $SERVER_PID
```

**Tasks**:
1. Add DataLoader for comments
2. Implement caching strategy
3. Monitor query performance
4. Compare with and without DataLoader

---

## Exercise 5: PostgreSQL Integration with Prisma

**Goal**: Use Prisma ORM with PostgreSQL.

### Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres psql -c "CREATE DATABASE graphql_prisma;"
sudo -u postgres psql -c "CREATE USER graphql_user WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE graphql_prisma TO graphql_user;"
```

### Setup Prisma Project
```bash
mkdir graphql-prisma-api && cd graphql-prisma-api
npm init -y
npm install apollo-server graphql @prisma/client
npm install -D prisma

# Initialize Prisma
npx prisma init
```

### Define Schema
```bash
cat > prisma/schema.prisma << 'EOF'
datasource db {
  provider = "postgresql"
  url      = "postgresql://graphql_user:password@localhost:5432/graphql_prisma"
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
EOF

# Run migration
npx prisma migrate dev --name init

# Generate Prisma Client
npx prisma generate
```

### Create Server
```bash
cat > server.js << 'EOF'
const { ApolloServer, gql } = require('apollo-server');
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

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

  type Query {
    users: [User!]!
    posts: [Post!]!
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
    createPost(title: String!, content: String!, authorId: Int!): Post!
  }
`;

const resolvers = {
  Query: {
    users: async () => await prisma.user.findMany(),
    posts: async () => await prisma.post.findMany()
  },

  Mutation: {
    createUser: async (_, { name, email }) => {
      return await prisma.user.create({
        data: { name, email }
      });
    },

    createPost: async (_, { title, content, authorId }) => {
      return await prisma.post.create({
        data: { title, content, authorId }
      });
    }
  },

  User: {
    posts: async (parent) => {
      return await prisma.post.findMany({
        where: { authorId: parent.id }
      });
    }
  },

  Post: {
    author: async (parent) => {
      return await prisma.user.findUnique({
        where: { id: parent.authorId }
      });
    }
  }
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
  console.log(`🚀 Prisma server ready at ${url}`);
});
EOF
```

**Tasks**:
1. Add more complex queries
2. Implement transactions
3. Add full-text search
4. Use Prisma's include for eager loading

---

## Challenge Exercises

1. **Build Complete Auth System**: Signup, login, password reset, email verification

2. **Multi-Database Support**: Support both MongoDB and PostgreSQL in same API

3. **Performance Comparison**: Measure query performance with/without DataLoader

4. **Migration Tool**: Create scripts to migrate data between databases

5. **Backup & Restore**: Implement database backup and restore functionality

---

## Verification Checklist

After completing Phase 4 exercises, you should be able to:

- [ ] Connect GraphQL to MongoDB
- [ ] Connect GraphQL to PostgreSQL
- [ ] Implement JWT authentication
- [ ] Hash passwords securely
- [ ] Protect resolvers with auth middleware
- [ ] Implement DataLoader for optimization
- [ ] Use Prisma ORM
- [ ] Handle database migrations
- [ ] Test authenticated endpoints
- [ ] Monitor query performance

---

## Next Steps

Ready for Phase 5!
- Build React frontend
- Deploy to production
- Add monitoring and logging
- Implement advanced features

**Excellent progress!** Your GraphQL API is production-ready!
