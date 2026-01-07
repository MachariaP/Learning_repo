# Phase 5: Terminal Exercises (Days 16+)

Practice production deployment, frontend integration, and DevOps tasks.

---

## Exercise 1: Create React App with Apollo Client

**Goal**: Build a React frontend that consumes your GraphQL API.

### Step 1: Setup React Project
```bash
# Create React app
npx create-react-app my-graphql-frontend
cd my-graphql-frontend

# Install Apollo Client
npm install @apollo/client graphql

# Start development server
npm start
```

### Step 2: Configure Apollo Client
```bash
cat > src/apollo-client.js << 'EOF'
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: 'http://localhost:4000/graphql',
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('authToken');
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
EOF
```

### Step 3: Create Components
```bash
mkdir src/components

cat > src/components/UserList.js << 'EOF'
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

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h2>Users</h2>
      <ul>
        {data.users.map(user => (
          <li key={user.id}>
            {user.name} - {user.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
EOF
```

**Tasks**:
1. Create a login component
2. Create a signup component
3. Create a posts list component
4. Implement protected routes

---

## Exercise 2: Docker Containerization

**Goal**: Containerize your GraphQL API.

### Step 1: Create Dockerfile
```bash
cd your-graphql-api

cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:4000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start application
CMD ["node", "server.js"]
EOF
```

### Step 2: Create docker-compose.yml
```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  api:
    build: .
    ports:
      - "4000:4000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=mongodb://mongo:27017/graphql
      - JWT_SECRET=your-secret-key
    depends_on:
      - mongo
    restart: unless-stopped

  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped

volumes:
  mongo-data:
EOF
```

### Step 3: Build and Run
```bash
# Build image
docker build -t my-graphql-api .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f api

# Test API
curl http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __typename }"}'

# Stop containers
docker-compose down
```

**Tasks**:
1. Add Redis to docker-compose
2. Add PostgreSQL option
3. Implement multi-stage builds
4. Add development vs production configurations

---

## Exercise 3: Environment Configuration

**Goal**: Properly manage environment variables for different environments.

### Step 1: Create Environment Files
```bash
# Development environment
cat > .env.development << 'EOF'
NODE_ENV=development
PORT=4000
DATABASE_URL=mongodb://localhost:27017/graphql_dev
JWT_SECRET=dev-secret-key
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=debug
ENABLE_PLAYGROUND=true
ENABLE_INTROSPECTION=true
EOF

# Production environment
cat > .env.production << 'EOF'
NODE_ENV=production
PORT=4000
DATABASE_URL=mongodb://production-server:27017/graphql_prod
JWT_SECRET=super-secret-production-key
ALLOWED_ORIGINS=https://myapp.com,https://www.myapp.com
LOG_LEVEL=error
ENABLE_PLAYGROUND=false
ENABLE_INTROSPECTION=false
SENTRY_DSN=your-sentry-dsn
APOLLO_KEY=your-apollo-key
EOF

# Add to .gitignore
echo ".env*" >> .gitignore
echo "!.env.example" >> .gitignore
```

### Step 2: Create Config Module
```bash
cat > config.js << 'EOF'
require('dotenv').config({
  path: `.env.${process.env.NODE_ENV || 'development'}`
});

module.exports = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT, 10) || 4000,
  database: {
    url: process.env.DATABASE_URL
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '7d'
  },
  cors: {
    origins: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000']
  },
  apollo: {
    playground: process.env.ENABLE_PLAYGROUND === 'true',
    introspection: process.env.ENABLE_INTROSPECTION === 'true'
  },
  logging: {
    level: process.env.LOG_LEVEL || 'info'
  }
};
EOF
```

**Tasks**:
1. Create environment validation
2. Add secrets rotation script
3. Create environment documentation
4. Set up CI/CD environment variables

---

## Exercise 4: Deploy to Heroku

**Goal**: Deploy your GraphQL API to Heroku.

### Step 1: Prepare for Deployment
```bash
# Install Heroku CLI
# Ubuntu/Debian:
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create Heroku app
heroku create my-unique-graphql-api

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Or set your own MongoDB URL
heroku config:set DATABASE_URL="your-mongodb-url"
```

### Step 2: Configure Environment
```bash
# Set environment variables
heroku config:set NODE_ENV=production
heroku config:set JWT_SECRET="$(openssl rand -base64 32)"
heroku config:set ALLOWED_ORIGINS="https://your-frontend.com"

# View all config
heroku config
```

### Step 3: Create Procfile
```bash
cat > Procfile << 'EOF'
web: node server.js
EOF
```

### Step 4: Deploy
```bash
# Add git remote
heroku git:remote -a my-unique-graphql-api

# Deploy
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Open app
heroku open

# View logs
heroku logs --tail
```

**Tasks**:
1. Set up automatic deploys from GitHub
2. Configure review apps
3. Set up staging environment
4. Implement zero-downtime deployments

---

## Exercise 5: Performance Testing

**Goal**: Benchmark and optimize your API performance.

### Step 1: Install Load Testing Tools
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Install Artillery
npm install -g artillery
```

### Step 2: Create Load Test Scripts
```bash
# Simple query test
cat > load-test.yml << 'EOF'
config:
  target: "http://localhost:4000"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Spike"

scenarios:
  - name: "Query users"
    engine: "http"
    flow:
      - post:
          url: "/graphql"
          json:
            query: "{ users { id name email } }"
          headers:
            Content-Type: "application/json"
EOF

# Run test
artillery run load-test.yml
```

### Step 3: Measure Performance
```bash
# Create performance test script
cat > perf-test.sh << 'EOF'
#!/bin/bash

API_URL="http://localhost:4000/graphql"

echo "=== GraphQL API Performance Test ==="
echo ""

# Test 1: Simple query
echo "Test 1: Simple query (100 requests)"
ab -n 100 -c 10 -p query.json -T application/json $API_URL

echo ""
echo "Test 2: Complex nested query (50 requests)"
ab -n 50 -c 5 -p complex-query.json -T application/json $API_URL

echo ""
echo "Done!"
EOF

chmod +x perf-test.sh

# Create query files
echo '{"query": "{ users { id name } }"}' > query.json
echo '{"query": "{ users { id name posts { id title comments { text } } } }"}' > complex-query.json

# Run tests
./perf-test.sh
```

**Tasks**:
1. Identify performance bottlenecks
2. Optimize slow queries
3. Add database indexes
4. Implement query batching

---

## Exercise 6: Monitoring and Logging

**Goal**: Set up comprehensive monitoring and logging.

### Step 1: Install Winston Logger
```bash
npm install winston
```

```bash
cat > logger.js << 'EOF'
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'graphql-api' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

module.exports = logger;
EOF
```

### Step 2: Create Monitoring Script
```bash
cat > monitor.sh << 'EOF'
#!/bin/bash

API_URL="http://localhost:4000"
LOG_FILE="monitor.log"

echo "Starting API monitoring..." | tee -a $LOG_FILE

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Health check
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health)
    
    if [ "$RESPONSE" = "200" ]; then
        echo "[$TIMESTAMP] ✓ API is healthy (HTTP $RESPONSE)" | tee -a $LOG_FILE
    else
        echo "[$TIMESTAMP] ✗ API is down (HTTP $RESPONSE)" | tee -a $LOG_FILE
        # Send alert (email, SMS, etc.)
    fi
    
    # Check response time
    RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" $API_URL/health)
    echo "[$TIMESTAMP] Response time: ${RESPONSE_TIME}s" | tee -a $LOG_FILE
    
    # Sleep for 30 seconds
    sleep 30
done
EOF

chmod +x monitor.sh
```

### Step 3: Set Up Log Rotation
```bash
cat > /etc/logrotate.d/graphql-api << 'EOF'
/path/to/your/app/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
EOF
```

**Tasks**:
1. Set up Prometheus metrics
2. Create Grafana dashboard
3. Configure alerts
4. Set up ELK stack for logs

---

## Exercise 7: CI/CD Pipeline

**Goal**: Automate testing and deployment.

### Step 1: Create GitHub Actions Workflow
```bash
mkdir -p .github/workflows

cat > .github/workflows/ci-cd.yml << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mongodb:
        image: mongo:6
        ports:
          - 27017:27017
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Run tests
      run: npm test
      env:
        DATABASE_URL: mongodb://localhost:27017/test
    
    - name: Build
      run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "my-graphql-api"
        heroku_email: "your-email@example.com"
EOF
```

### Step 2: Create Test Scripts
```bash
# Add to package.json
cat > package.json << 'EOF'
{
  "name": "graphql-api",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest --coverage",
    "lint": "eslint .",
    "build": "echo 'Build step if needed'"
  }
}
EOF
```

**Tasks**:
1. Add code coverage reporting
2. Set up automatic security scanning
3. Add deployment to staging
4. Implement rollback mechanism

---

## Exercise 8: Implement Caching

**Goal**: Add Redis caching for better performance.

### Step 1: Install Redis
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis
redis-cli ping
```

### Step 2: Install Redis Client
```bash
npm install redis
```

### Step 3: Implement Caching
```bash
cat > cache.js << 'EOF'
const redis = require('redis');

const client = redis.createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

client.on('error', (err) => console.error('Redis error:', err));

(async () => {
  await client.connect();
})();

const cache = {
  get: async (key) => {
    try {
      const data = await client.get(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  },

  set: async (key, value, ttl = 3600) => {
    try {
      await client.setEx(key, ttl, JSON.stringify(value));
    } catch (error) {
      console.error('Cache set error:', error);
    }
  },

  del: async (key) => {
    try {
      await client.del(key);
    } catch (error) {
      console.error('Cache delete error:', error);
    }
  },

  flush: async () => {
    try {
      await client.flushAll();
    } catch (error) {
      console.error('Cache flush error:', error);
    }
  }
};

module.exports = cache;
EOF
```

### Step 4: Use in Resolvers
```bash
cat > cached-resolvers.js << 'EOF'
const cache = require('./cache');

const resolvers = {
  Query: {
    user: async (_, { id }) => {
      const cacheKey = `user:${id}`;
      
      // Check cache
      const cached = await cache.get(cacheKey);
      if (cached) {
        console.log('Cache hit for user:', id);
        return cached;
      }
      
      // Fetch from database
      const user = await User.findById(id);
      
      // Store in cache (1 hour)
      await cache.set(cacheKey, user, 3600);
      
      return user;
    }
  },

  Mutation: {
    updateUser: async (_, { id, input }) => {
      const user = await User.findByIdAndUpdate(id, input, { new: true });
      
      // Invalidate cache
      await cache.del(`user:${id}`);
      
      return user;
    }
  }
};

module.exports = resolvers;
EOF
```

**Tasks**:
1. Implement cache warming
2. Add cache invalidation strategies
3. Monitor cache hit rates
4. Implement distributed caching

---

## Challenge Exercises

1. **Full Production Stack**: Deploy API + Frontend + Database + Redis + Monitoring

2. **Zero-Downtime Deployment**: Implement blue-green deployment

3. **Auto-Scaling**: Configure auto-scaling based on load

4. **Disaster Recovery**: Implement backup and recovery procedures

5. **Multi-Region Deployment**: Deploy to multiple regions

6. **GraphQL Federation**: Split monolith into microservices

---

## Production Deployment Checklist

```bash
# Create deployment checklist script
cat > deployment-checklist.sh << 'EOF'
#!/bin/bash

echo "=== Pre-Deployment Checklist ==="
echo ""

checks=(
  "Environment variables configured:check_env_vars"
  "Database backups enabled:check_backups"
  "SSL certificate valid:check_ssl"
  "Health check endpoint working:check_health"
  "Rate limiting enabled:check_rate_limit"
  "Monitoring configured:check_monitoring"
  "Error tracking active:check_error_tracking"
  "CI/CD pipeline green:check_ci_cd"
  "Documentation updated:check_docs"
  "Team notified:check_team"
)

passed=0
failed=0

for check in "${checks[@]}"; do
    IFS=':' read -r name func <<< "$check"
    echo -n "Checking: $name ... "
    
    # Simulate check (replace with actual checks)
    if [ $((RANDOM % 2)) -eq 0 ]; then
        echo "✓ PASS"
        ((passed++))
    else
        echo "✗ FAIL"
        ((failed++))
    fi
done

echo ""
echo "Results: $passed passed, $failed failed"

if [ $failed -eq 0 ]; then
    echo "🎉 Ready for deployment!"
    exit 0
else
    echo "❌ Fix issues before deploying!"
    exit 1
fi
EOF

chmod +x deployment-checklist.sh
```

---

## Verification Checklist

After completing Phase 5 exercises, you should be able to:

- [ ] Build React apps with Apollo Client
- [ ] Containerize applications with Docker
- [ ] Deploy to cloud platforms (Heroku, Railway, AWS)
- [ ] Configure environment variables properly
- [ ] Implement caching with Redis
- [ ] Set up logging and monitoring
- [ ] Create CI/CD pipelines
- [ ] Perform load testing
- [ ] Implement zero-downtime deployments
- [ ] Handle production incidents

---

## Congratulations!

You've completed the entire GraphQL learning path! You now have:
- Built GraphQL APIs from scratch
- Connected to databases
- Implemented authentication
- Optimized performance
- Deployed to production
- Built React frontends
- Set up monitoring and CI/CD

**You are now a GraphQL developer! 🚀**

Keep practicing, building, and contributing to the GraphQL community!
