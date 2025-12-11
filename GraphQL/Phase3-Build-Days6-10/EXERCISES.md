# Phase 3: Terminal Exercises (Days 6-10)

Build and test your own GraphQL servers from the terminal.

---

## Exercise 1: Setup Your First GraphQL Server

**Goal**: Create a minimal GraphQL server.

### Step 1: Create Project
```bash
# Create project directory
mkdir graphql-hello && cd graphql-hello

# Initialize npm project
npm init -y

# Install dependencies
npm install apollo-server graphql

# Verify installation
npm list apollo-server graphql
```

### Step 2: Create Server File
```bash
cat > server.js << 'EOF'
const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type Query {
    hello: String
    greeting(name: String!): String
  }
`;

const resolvers = {
  Query: {
    hello: () => 'Hello, GraphQL!',
    greeting: (parent, args) => `Hello, ${args.name}!`
  }
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
EOF
```

### Step 3: Start Server
```bash
# Start the server
node server.js

# Server runs on http://localhost:4000
# Press Ctrl+C to stop
```

### Step 4: Test from Terminal
```bash
# In a new terminal, test the API
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ hello }"}'

curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { greeting(name: \"Alice\") }"}'
```

**Tasks**:
1. Add a `goodbye` query that returns "Goodbye, GraphQL!"
2. Add a query that returns the current time
3. Add a query that accepts age and returns a message

---

## Exercise 2: Build a Todo API

**Goal**: Create a complete CRUD API for todos.

### Step 1: Create Project Structure
```bash
mkdir graphql-todo-api && cd graphql-todo-api
npm init -y
npm install apollo-server graphql

# Create file structure
mkdir src
touch src/data.js src/schema.js src/resolvers.js src/server.js
```

### Step 2: Create Data Store
```bash
cat > src/data.js << 'EOF'
let todos = [
  {
    id: '1',
    title: 'Learn GraphQL',
    completed: true,
    createdAt: new Date().toISOString()
  },
  {
    id: '2',
    title: 'Build GraphQL API',
    completed: false,
    createdAt: new Date().toISOString()
  }
];

let nextId = 3;

module.exports = {
  todos,
  getNextId: () => String(nextId++)
};
EOF
```

### Step 3: Create Schema
```bash
cat > src/schema.js << 'EOF'
const { gql } = require('apollo-server');

const typeDefs = gql`
  type Todo {
    id: ID!
    title: String!
    completed: Boolean!
    createdAt: String!
  }

  type Query {
    todos: [Todo!]!
    todo(id: ID!): Todo
    completedTodos: [Todo!]!
  }

  type Mutation {
    createTodo(title: String!): Todo!
    toggleTodo(id: ID!): Todo!
    deleteTodo(id: ID!): DeleteResponse!
  }

  type DeleteResponse {
    success: Boolean!
    message: String!
  }
`;

module.exports = typeDefs;
EOF
```

### Step 4: Create Resolvers
```bash
cat > src/resolvers.js << 'EOF'
const { UserInputError } = require('apollo-server');
const { todos, getNextId } = require('./data');

const resolvers = {
  Query: {
    todos: () => todos,
    
    todo: (_, { id }) => {
      const todo = todos.find(t => t.id === id);
      if (!todo) {
        throw new UserInputError('Todo not found');
      }
      return todo;
    },
    
    completedTodos: () => todos.filter(t => t.completed)
  },

  Mutation: {
    createTodo: (_, { title }) => {
      if (!title || title.trim().length === 0) {
        throw new UserInputError('Title cannot be empty');
      }

      const newTodo = {
        id: getNextId(),
        title: title.trim(),
        completed: false,
        createdAt: new Date().toISOString()
      };

      todos.push(newTodo);
      return newTodo;
    },

    toggleTodo: (_, { id }) => {
      const todo = todos.find(t => t.id === id);
      if (!todo) {
        throw new UserInputError('Todo not found');
      }

      todo.completed = !todo.completed;
      return todo;
    },

    deleteTodo: (_, { id }) => {
      const index = todos.findIndex(t => t.id === id);
      
      if (index === -1) {
        return {
          success: false,
          message: `Todo with ID ${id} not found`
        };
      }

      todos.splice(index, 1);
      return {
        success: true,
        message: 'Todo deleted successfully'
      };
    }
  }
};

module.exports = resolvers;
EOF
```

### Step 5: Create Server
```bash
cat > src/server.js << 'EOF'
const { ApolloServer } = require('apollo-server');
const typeDefs = require('./schema');
const resolvers = require('./resolvers');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: () => ({
    timestamp: new Date().toISOString()
  })
});

server.listen().then(({ url }) => {
  console.log(`🚀 Todo API ready at ${url}`);
});
EOF
```

### Step 6: Test the API
```bash
# Start server
node src/server.js &
SERVER_PID=$!
sleep 2

# Test queries
echo "=== Get all todos ==="
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ todos { id title completed } }"}' | jq '.'

echo ""
echo "=== Create todo ==="
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createTodo(title: \"Test from terminal\") { id title completed } }"}' | jq '.'

echo ""
echo "=== Get completed todos ==="
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ completedTodos { id title } }"}' | jq '.'

# Stop server
kill $SERVER_PID
```

**Tasks**:
1. Add an `updateTodo` mutation that can change the title
2. Add a query to get todos by status
3. Add timestamps for when todos are updated
4. Add a counter for total todos

---

## Exercise 3: Build a Blog API with Relationships

**Goal**: Create an API with User, Post, and Comment relationships.

### Create the Project
```bash
mkdir graphql-blog-api && cd graphql-blog-api
npm init -y
npm install apollo-server graphql
```

### Create Complete Blog API
```bash
cat > blog-server.js << 'EOF'
const { ApolloServer, gql, UserInputError } = require('apollo-server');

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
    comments: [Comment!]!
  }

  type Comment {
    id: ID!
    text: String!
    author: User!
    post: Post!
    createdAt: String!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
    posts: [Post!]!
    post(id: ID!): Post
    publishedPosts: [Post!]!
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
    createPost(title: String!, content: String!, authorId: ID!): Post!
    publishPost(id: ID!): Post!
    createComment(postId: ID!, authorId: ID!, text: String!): Comment!
  }
`;

// In-memory data
let users = [
  { id: '1', name: 'Alice Johnson', email: 'alice@example.com' },
  { id: '2', name: 'Bob Smith', email: 'bob@example.com' }
];

let posts = [
  { id: '1', title: 'GraphQL Basics', content: 'Content here...', published: true, authorId: '1' }
];

let comments = [];

let nextUserId = 3;
let nextPostId = 2;
let nextCommentId = 1;

// Resolvers
const resolvers = {
  Query: {
    users: () => users,
    user: (_, { id }) => users.find(u => u.id === id),
    posts: () => posts,
    post: (_, { id }) => posts.find(p => p.id === id),
    publishedPosts: () => posts.filter(p => p.published)
  },

  Mutation: {
    createUser: (_, { name, email }) => {
      const user = {
        id: String(nextUserId++),
        name,
        email
      };
      users.push(user);
      return user;
    },

    createPost: (_, { title, content, authorId }) => {
      const author = users.find(u => u.id === authorId);
      if (!author) {
        throw new UserInputError('Author not found');
      }

      const post = {
        id: String(nextPostId++),
        title,
        content,
        published: false,
        authorId
      };

      posts.push(post);
      return post;
    },

    publishPost: (_, { id }) => {
      const post = posts.find(p => p.id === id);
      if (!post) {
        throw new UserInputError('Post not found');
      }

      post.published = true;
      return post;
    },

    createComment: (_, { postId, authorId, text }) => {
      const post = posts.find(p => p.id === postId);
      const author = users.find(u => u.id === authorId);

      if (!post) throw new UserInputError('Post not found');
      if (!author) throw new UserInputError('Author not found');

      const comment = {
        id: String(nextCommentId++),
        text,
        postId,
        authorId,
        createdAt: new Date().toISOString()
      };

      comments.push(comment);
      return comment;
    }
  },

  User: {
    posts: (parent) => posts.filter(p => p.authorId === parent.id)
  },

  Post: {
    author: (parent) => users.find(u => u.id === parent.authorId),
    comments: (parent) => comments.filter(c => c.postId === parent.id)
  },

  Comment: {
    author: (parent) => users.find(u => u.id === parent.authorId),
    post: (parent) => posts.find(p => p.id === parent.postId)
  }
};

// Server
const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
  console.log(`🚀 Blog API ready at ${url}`);
});
EOF
```

### Test the Blog API
```bash
# Start server in background
node blog-server.js &
SERVER_PID=$!
sleep 2

# Test complex nested query
echo "=== Get users with their posts ==="
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ users { name posts { title published } } }"
  }' | jq '.'

# Create a post
echo ""
echo "=== Create a post ==="
curl -s -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createPost(title: \"My Post\", content: \"Content\", authorId: \"1\") { id title author { name } } }"
  }' | jq '.'

# Stop server
kill $SERVER_PID
```

**Tasks**:
1. Add a `deletePost` mutation
2. Add a query to get posts by a specific author
3. Add like count to posts
4. Add pagination to the posts query

---

## Exercise 4: Testing Your API with Scripts

**Goal**: Create automated test scripts for your API.

### Create Test Script
```bash
cat > test-api.sh << 'EOF'
#!/bin/bash

API_URL="http://localhost:4000/graphql"

echo "=== GraphQL API Test Suite ==="
echo ""

# Test 1: Get all todos
echo "Test 1: Get all todos"
RESPONSE=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"query": "{ todos { id title } }"}')

TODO_COUNT=$(echo "$RESPONSE" | jq '.data.todos | length')
echo "✓ Found $TODO_COUNT todos"
echo ""

# Test 2: Create a todo
echo "Test 2: Create a todo"
RESPONSE=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createTodo(title: \"Test Todo\") { id title completed } }"}')

NEW_TODO_ID=$(echo "$RESPONSE" | jq -r '.data.createTodo.id')
echo "✓ Created todo with ID: $NEW_TODO_ID"
echo ""

# Test 3: Get specific todo
echo "Test 3: Get specific todo"
RESPONSE=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"{ todo(id: \\\"$NEW_TODO_ID\\\") { title completed } }\"}")

TODO_TITLE=$(echo "$RESPONSE" | jq -r '.data.todo.title')
echo "✓ Retrieved todo: $TODO_TITLE"
echo ""

# Test 4: Toggle todo
echo "Test 4: Toggle todo"
RESPONSE=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"mutation { toggleTodo(id: \\\"$NEW_TODO_ID\\\") { completed } }\"}")

IS_COMPLETED=$(echo "$RESPONSE" | jq -r '.data.toggleTodo.completed')
echo "✓ Todo completed status: $IS_COMPLETED"
echo ""

# Test 5: Delete todo
echo "Test 5: Delete todo"
RESPONSE=$(curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"mutation { deleteTodo(id: \\\"$NEW_TODO_ID\\\") { success message } }\"}")

SUCCESS=$(echo "$RESPONSE" | jq -r '.data.deleteTodo.success')
echo "✓ Delete success: $SUCCESS"
echo ""

echo "=== All tests passed! ==="
EOF

chmod +x test-api.sh
```

### Run Tests
```bash
# Start your server first
node src/server.js &
sleep 2

# Run tests
./test-api.sh

# Stop server
killall node
```

**Tasks**:
1. Add error handling to the test script
2. Create tests for edge cases (empty title, invalid ID)
3. Add performance timing to each test
4. Create a test report generator

---

## Exercise 5: API Performance Monitoring

**Goal**: Monitor and measure your API's performance.

### Create Performance Monitor
```bash
cat > perf-test.sh << 'EOF'
#!/bin/bash

API_URL="http://localhost:4000/graphql"
QUERY='{"query": "{ todos { id title completed } }"}'

echo "=== GraphQL API Performance Test ==="
echo ""

# Warm-up request
curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d "$QUERY" > /dev/null

# Run 10 requests and measure time
TOTAL_TIME=0
REQUESTS=10

echo "Running $REQUESTS requests..."

for i in $(seq 1 $REQUESTS); do
    START=$(date +%s%N)
    
    curl -s -X POST $API_URL \
      -H "Content-Type: application/json" \
      -d "$QUERY" > /dev/null
    
    END=$(date +%s%N)
    TIME=$((($END - $START) / 1000000))  # Convert to milliseconds
    TOTAL_TIME=$(($TOTAL_TIME + $TIME))
    
    echo "Request $i: ${TIME}ms"
done

AVG_TIME=$(($TOTAL_TIME / $REQUESTS))

echo ""
echo "Results:"
echo "  Total requests: $REQUESTS"
echo "  Total time: ${TOTAL_TIME}ms"
echo "  Average time: ${AVG_TIME}ms"
EOF

chmod +x perf-test.sh
```

**Tasks**:
1. Compare performance of simple vs complex queries
2. Test performance with different data sizes
3. Monitor memory usage
4. Create a performance baseline

---

## Exercise 6: Build a CLI for Your API

**Goal**: Create a command-line interface for interacting with your API.

```bash
cat > graphql-cli.sh << 'EOF'
#!/bin/bash

API_URL="http://localhost:4000/graphql"

show_help() {
    echo "GraphQL Todo CLI"
    echo ""
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  list                - List all todos"
    echo "  add <title>         - Add a new todo"
    echo "  toggle <id>         - Toggle todo completion"
    echo "  delete <id>         - Delete a todo"
    echo "  completed           - List completed todos"
    echo ""
}

list_todos() {
    curl -s -X POST $API_URL \
      -H "Content-Type: application/json" \
      -d '{"query": "{ todos { id title completed } }"}' | \
      jq -r '.data.todos[] | "\(.id): [\(if .completed then "✓" else " " end)] \(.title)"'
}

add_todo() {
    TITLE=$1
    curl -s -X POST $API_URL \
      -H "Content-Type: application/json" \
      -d "{\"query\": \"mutation { createTodo(title: \\\"$TITLE\\\") { id title } }\"}" | \
      jq -r '"Created: \(.data.createTodo.title)"'
}

toggle_todo() {
    ID=$1
    curl -s -X POST $API_URL \
      -H "Content-Type: application/json" \
      -d "{\"query\": \"mutation { toggleTodo(id: \\\"$ID\\\") { id completed } }\"}" | \
      jq -r '"Todo \(.data.toggleTodo.id) completed: \(.data.toggleTodo.completed)"'
}

delete_todo() {
    ID=$1
    curl -s -X POST $API_URL \
      -H "Content-Type: application/json" \
      -d "{\"query\": \"mutation { deleteTodo(id: \\\"$ID\\\") { success message } }\"}" | \
      jq -r '.data.deleteTodo.message'
}

list_completed() {
    curl -s -X POST $API_URL \
      -H "Content-Type: application/json" \
      -d '{"query": "{ completedTodos { id title } }"}' | \
      jq -r '.data.completedTodos[] | "\(.id): \(.title)"'
}

case $1 in
    list)
        list_todos
        ;;
    add)
        add_todo "$2"
        ;;
    toggle)
        toggle_todo "$2"
        ;;
    delete)
        delete_todo "$2"
        ;;
    completed)
        list_completed
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
EOF

chmod +x graphql-cli.sh

# Test it
./graphql-cli.sh help
```

**Tasks**:
1. Add color output to the CLI
2. Add a search command
3. Add batch operations (delete all completed)
4. Add data export functionality

---

## Challenge Exercises

1. **Build a Recipe API**: Users, Recipes, Ingredients, Reviews
2. **Build a Social Media API**: Users, Posts, Comments, Likes, Follows
3. **Build an E-commerce API**: Products, Categories, Orders, Cart
4. **Add File Upload**: Implement file upload for user avatars
5. **Add Subscriptions**: Real-time updates using GraphQL subscriptions

---

## Verification Checklist

After completing Phase 3 exercises, you should be able to:

- [ ] Set up a GraphQL server from scratch
- [ ] Define schemas with multiple types
- [ ] Implement query resolvers
- [ ] Implement mutation resolvers
- [ ] Handle relationships between types
- [ ] Test APIs from the terminal
- [ ] Create test automation scripts
- [ ] Monitor API performance
- [ ] Build CLI tools for your API
- [ ] Structure GraphQL projects properly

---

## Next Steps

You're ready for Phase 4!
- Connect to databases (MongoDB, PostgreSQL)
- Implement authentication
- Use DataLoader for optimization
- Add validation and security

**Great job!** You've built real GraphQL APIs!
