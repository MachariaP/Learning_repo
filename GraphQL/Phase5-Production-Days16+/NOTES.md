# Phase 5: Production Deployment and Frontend Integration (Days 16+)

## Learning Objectives
By the end of this phase, you should:
- Build React frontends with Apollo Client
- Deploy GraphQL APIs to production
- Implement error handling and logging
- Add monitoring and analytics
- Implement caching strategies
- Handle production security concerns
- Optimize for performance

---

## Day 16-18: Frontend with Apollo Client

### Setting Up React with Apollo Client

**Create React App:**
```bash
npx create-react-app graphql-react-app
cd graphql-react-app
npm install @apollo/client graphql
```

**Setup Apollo Client:**
```javascript
// src/apollo.js
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: 'http://localhost:4000/graphql',
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  };
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});

export default client;
```

**Wrap App with Apollo Provider:**
```javascript
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ApolloProvider } from '@apollo/client';
import App from './App';
import client from './apollo';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </React.StrictMode>
);
```

### Queries in React

**Using useQuery Hook:**
```javascript
// src/components/UserList.js
import { useQuery, gql } from '@apollo/client';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function UserList() {
  const { loading, error, data } = useQuery(GET_USERS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {data.users.map(user => (
          <li key={user.id}>
            {user.name} ({user.email})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
```

**Query with Variables:**
```javascript
// src/components/UserDetail.js
import { useQuery, gql } from '@apollo/client';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
      posts {
        id
        title
      }
    }
  }
`;

function UserDetail({ userId }) {
  const { loading, error, data } = useQuery(GET_USER, {
    variables: { id: userId }
  });

  if (loading) return <p>Loading user...</p>;
  if (error) return <p>Error: {error.message}</p>;

  const user = data.user;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <h3>Posts:</h3>
      <ul>
        {user.posts.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserDetail;
```

### Mutations in React

**Using useMutation Hook:**
```javascript
// src/components/CreateUser.js
import { useState } from 'react';
import { useMutation, gql } from '@apollo/client';

const CREATE_USER = gql`
  mutation CreateUser($name: String!, $email: String!) {
    createUser(name: $name, email: $email) {
      id
      name
      email
    }
  }
`;

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function CreateUser() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const [createUser, { loading, error }] = useMutation(CREATE_USER, {
    // Refetch queries after mutation
    refetchQueries: [{ query: GET_USERS }],
    // Or update cache manually
    update(cache, { data: { createUser } }) {
      const { users } = cache.readQuery({ query: GET_USERS });
      cache.writeQuery({
        query: GET_USERS,
        data: { users: [...users, createUser] }
      });
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    createUser({ variables: { name, email } });
    setName('');
    setEmail('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create User'}
      </button>
      {error && <p>Error: {error.message}</p>}
    </form>
  );
}

export default CreateUser;
```

### Authentication in React

**Login Component:**
```javascript
// src/components/Login.js
import { useState } from 'react';
import { useMutation, gql } from '@apollo/client';
import { useNavigate } from 'react-router-dom';

const LOGIN = gql`
  mutation Login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      token
      user {
        id
        name
        email
      }
    }
  }
`;

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const [login, { loading, error }] = useMutation(LOGIN, {
    onCompleted: (data) => {
      localStorage.setItem('token', data.login.token);
      navigate('/dashboard');
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    login({ variables: { email, password } });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
      {error && <p>Error: {error.message}</p>}
    </form>
  );
}

export default Login;
```

---

## Day 19-20: Production Deployment

### Preparing for Production

**Environment Variables:**
```javascript
// Use .env file
// .env
DATABASE_URL=mongodb://prod-server:27017/myapp
JWT_SECRET=your-super-secret-key-here
PORT=4000
NODE_ENV=production
```

```javascript
// server.js
require('dotenv').config();

const PORT = process.env.PORT || 4000;
const JWT_SECRET = process.env.JWT_SECRET;

mongoose.connect(process.env.DATABASE_URL);

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  playground: process.env.NODE_ENV !== 'production'
});
```

### Security Best Practices

**1. Disable Introspection in Production:**
```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: false, // Disable in production
  playground: false     // Disable in production
});
```

**2. Add Rate Limiting:**
```bash
npm install express-rate-limit
```

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/graphql', limiter);
```

**3. Query Complexity Limits:**
```bash
npm install graphql-query-complexity
```

```javascript
const { createComplexityLimitRule } = require('graphql-query-complexity');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000) // Max complexity score
  ]
});
```

**4. CORS Configuration:**
```bash
npm install cors
```

```javascript
const cors = require('cors');

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS.split(','),
  credentials: true
}));
```

### Deployment Options

**Option 1: Heroku**
```bash
# Install Heroku CLI
heroku create my-graphql-api

# Add environment variables
heroku config:set DATABASE_URL=your-db-url
heroku config:set JWT_SECRET=your-secret

# Create Procfile
echo "web: node server.js" > Procfile

# Deploy
git push heroku main
```

**Option 2: Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Option 3: DigitalOcean App Platform**
- Connect GitHub repository
- Configure environment variables
- Auto-deploys on push

**Option 4: AWS (EC2 + RDS)**
```bash
# Install PM2 for process management
npm install -g pm2

# Start server with PM2
pm2 start server.js --name graphql-api

# Save PM2 configuration
pm2 save
pm2 startup
```

**Option 5: Docker**
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 4000

CMD ["node", "server.js"]
```

```bash
# Build and run
docker build -t my-graphql-api .
docker run -p 4000:4000 --env-file .env my-graphql-api
```

---

## Day 21+: Monitoring and Optimization

### Error Logging

**Winston Logger:**
```bash
npm install winston
```

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Use in resolvers
const resolvers = {
  Query: {
    users: async () => {
      try {
        logger.info('Fetching users');
        return await User.find();
      } catch (error) {
        logger.error('Error fetching users:', error);
        throw error;
      }
    }
  }
};
```

**Sentry Integration:**
```bash
npm install @sentry/node
```

```javascript
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (error) => {
    Sentry.captureException(error);
    return error;
  }
});
```

### Performance Monitoring

**Apollo Studio:**
```javascript
const { ApolloServer } = require('apollo-server');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    require('apollo-server-core').ApolloServerPluginUsageReporting({
      apiKey: process.env.APOLLO_KEY
    })
  ]
});
```

**Custom Metrics:**
```javascript
const metrics = {
  queryCount: 0,
  mutationCount: 0,
  errorCount: 0
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    {
      requestDidStart() {
        return {
          didResolveOperation({ operation }) {
            if (operation.operation === 'query') {
              metrics.queryCount++;
            } else if (operation.operation === 'mutation') {
              metrics.mutationCount++;
            }
          },
          didEncounterErrors() {
            metrics.errorCount++;
          }
        };
      }
    }
  ]
});

// Expose metrics endpoint
app.get('/metrics', (req, res) => {
  res.json(metrics);
});
```

### Caching Strategies

**Redis Caching:**
```bash
npm install redis
```

```javascript
const redis = require('redis');
const client = redis.createClient();

const resolvers = {
  Query: {
    user: async (_, { id }) => {
      // Check cache first
      const cached = await client.get(`user:${id}`);
      if (cached) {
        return JSON.parse(cached);
      }

      // Fetch from database
      const user = await User.findById(id);

      // Store in cache (expire after 1 hour)
      await client.setEx(`user:${id}`, 3600, JSON.stringify(user));

      return user;
    }
  }
};
```

**Response Caching:**
```bash
npm install apollo-server-plugin-response-cache
```

```javascript
const { ApolloServer } = require('apollo-server');
const responseCachePlugin = require('apollo-server-plugin-response-cache');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [responseCachePlugin()],
  cacheControl: {
    defaultMaxAge: 60 // 60 seconds
  }
});

// In schema, add cache hints
const typeDefs = gql`
  type Query {
    users: [User!]! @cacheControl(maxAge: 300)
  }
`;
```

---

## Production Checklist

### Before Deployment

- [ ] **Environment Variables**: All secrets in env vars
- [ ] **Database**: Production database configured
- [ ] **Authentication**: JWT secrets changed
- [ ] **CORS**: Allowed origins configured
- [ ] **Rate Limiting**: Implemented
- [ ] **Query Complexity**: Limited
- [ ] **Introspection**: Disabled in production
- [ ] **Error Handling**: Proper error messages
- [ ] **Logging**: Centralized logging setup
- [ ] **Monitoring**: Error tracking configured
- [ ] **Tests**: All tests passing
- [ ] **Documentation**: API documented
- [ ] **Backups**: Database backup strategy
- [ ] **SSL/TLS**: HTTPS enabled
- [ ] **Health Check**: Health check endpoint

### After Deployment

- [ ] **Smoke Tests**: Basic functionality works
- [ ] **Load Testing**: API handles expected load
- [ ] **Monitoring**: Metrics being collected
- [ ] **Alerts**: Error alerts configured
- [ ] **Rollback Plan**: Can revert if needed
- [ ] **Documentation**: Updated with prod URLs
- [ ] **Team Training**: Team knows how to operate

---

## Advanced Topics

### GraphQL Subscriptions (Real-time)

```javascript
const { ApolloServer, gql, PubSub } = require('apollo-server');

const pubsub = new PubSub();

const typeDefs = gql`
  type Subscription {
    postCreated: Post!
  }
`;

const resolvers = {
  Mutation: {
    createPost: async (_, args) => {
      const post = await Post.create(args);
      
      // Publish event
      pubsub.publish('POST_CREATED', { postCreated: post });
      
      return post;
    }
  },
  
  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator(['POST_CREATED'])
    }
  }
};
```

### File Uploads

```javascript
const { GraphQLUpload } = require('graphql-upload');

const typeDefs = gql`
  scalar Upload

  type Mutation {
    uploadFile(file: Upload!): File!
  }
`;

const resolvers = {
  Upload: GraphQLUpload,
  
  Mutation: {
    uploadFile: async (_, { file }) => {
      const { createReadStream, filename } = await file;
      const stream = createReadStream();
      
      // Save file logic here
      
      return { filename, url: `/uploads/${filename}` };
    }
  }
};
```

---

## Summary: Production-Ready Checklist

**Backend:**
- ✅ Environment variables configured
- ✅ Database connection pooling
- ✅ Authentication & authorization
- ✅ DataLoader for performance
- ✅ Error handling & logging
- ✅ Rate limiting
- ✅ Query complexity limits
- ✅ Caching strategy
- ✅ Monitoring & alerts

**Frontend:**
- ✅ Apollo Client configured
- ✅ Error boundaries
- ✅ Loading states
- ✅ Optimistic updates
- ✅ Cache management
- ✅ Authentication flow
- ✅ Production build optimized

**DevOps:**
- ✅ CI/CD pipeline
- ✅ Automated tests
- ✅ Database migrations
- ✅ Backup strategy
- ✅ SSL certificate
- ✅ Domain configured
- ✅ Monitoring dashboard
- ✅ Log aggregation

---

## Congratulations!

You've completed the GraphQL learning path! You now have the knowledge to:
- Build GraphQL APIs from scratch
- Connect to databases
- Implement authentication
- Optimize performance
- Deploy to production
- Build React frontends
- Monitor and maintain your APIs

**Keep Learning:**
- Explore GraphQL Federation for microservices
- Learn about GraphQL Code Generators
- Study advanced caching strategies
- Contribute to GraphQL open-source projects

**Happy coding! 🚀**
