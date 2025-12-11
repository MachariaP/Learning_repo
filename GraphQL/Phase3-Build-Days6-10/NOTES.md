# Phase 3: Build Your First GraphQL Server (Days 6-10)

## Learning Objectives
By the end of this phase, you should:
- Set up a GraphQL server with Apollo Server
- Define your own schemas using SDL
- Implement resolvers for queries and mutations
- Work with in-memory data
- Understand the resolver chain
- Handle relationships between types
- Implement basic error handling

---

## Day 6: Server Setup and Basic Schema

### Why Apollo Server?

**Apollo Server** is the industry-standard GraphQL server for Node.js.

**Advantages:**
- Easy to set up
- Great documentation
- Built-in GraphQL playground
- Excellent TypeScript support
- Production-ready features
- Large community

**Alternatives:**
- GraphQL Yoga (batteries-included)
- Express-GraphQL (minimal)
- Mercurius (Fastify - high performance)

### Project Setup

**Step 1: Initialize Project**
```bash
mkdir my-graphql-server
cd my-graphql-server
npm init -y
```

**Step 2: Install Dependencies**
```bash
npm install apollo-server graphql
```

**Step 3: Create Server File**
```javascript
// server.js
const { ApolloServer, gql } = require('apollo-server');

// Define your schema
const typeDefs = gql`
  type Query {
    hello: String
  }
`;

// Define your resolvers
const resolvers = {
  Query: {
    hello: () => 'Hello, GraphQL World!'
  }
};

// Create server instance
const server = new ApolloServer({
  typeDefs,
  resolvers
});

// Start the server
server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
```

**Step 4: Run the Server**
```bash
node server.js
```

**Step 5: Test in Browser**
- Open `http://localhost:4000`
- Try the query: `{ hello }`

### Understanding the Structure

**1. Type Definitions (typeDefs):**
- Define your schema using SDL
- Wrapped in `gql` template literal
- Describes what data is available

**2. Resolvers:**
- Functions that fetch the data
- Match the structure of your schema
- Return the actual data

**3. ApolloServer:**
- Combines typeDefs and resolvers
- Starts HTTP server
- Provides GraphQL playground

### Building a Todo API

Let's build a simple todo list API.

**Complete Schema:**
```graphql
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
  updateTodo(id: ID!, title: String, completed: Boolean): Todo!
  deleteTodo(id: ID!): DeleteResponse!
}

type DeleteResponse {
  success: Boolean!
  message: String!
}
```

---

## Day 7: Implementing Resolvers

### In-Memory Data Store

```javascript
// data.js
let todos = [
  {
    id: '1',
    title: 'Learn GraphQL basics',
    completed: true,
    createdAt: new Date().toISOString()
  },
  {
    id: '2',
    title: 'Build GraphQL server',
    completed: false,
    createdAt: new Date().toISOString()
  }
];

let nextId = 3;

module.exports = {
  todos,
  getNextId: () => String(nextId++)
};
```

### Query Resolvers

```javascript
const { todos, getNextId } = require('./data');

const resolvers = {
  Query: {
    // Get all todos
    todos: () => todos,
    
    // Get single todo by ID
    todo: (parent, args) => {
      return todos.find(todo => todo.id === args.id);
    },
    
    // Get completed todos
    completedTodos: () => {
      return todos.filter(todo => todo.completed);
    }
  }
};
```

### Resolver Function Signature

Every resolver receives four arguments:

```javascript
fieldName: (parent, args, context, info) => {
  // parent: Result from parent resolver
  // args: Arguments passed to the field
  // context: Shared across all resolvers (auth, db, etc.)
  // info: Field metadata (rarely used)
  return data;
}
```

**Example with All Parameters:**
```javascript
todo: (parent, args, context, info) => {
  console.log('Parent:', parent);           // undefined for root queries
  console.log('Args:', args);               // { id: "1" }
  console.log('Context:', context);         // { user, db, etc. }
  console.log('Field Name:', info.fieldName); // "todo"
  
  return todos.find(t => t.id === args.id);
}
```

### Mutation Resolvers

```javascript
const resolvers = {
  Query: {
    // ... query resolvers
  },
  
  Mutation: {
    // Create a new todo
    createTodo: (parent, args) => {
      const newTodo = {
        id: getNextId(),
        title: args.title,
        completed: false,
        createdAt: new Date().toISOString()
      };
      
      todos.push(newTodo);
      return newTodo;
    },
    
    // Update existing todo
    updateTodo: (parent, args) => {
      const todo = todos.find(t => t.id === args.id);
      
      if (!todo) {
        throw new Error(`Todo with ID ${args.id} not found`);
      }
      
      // Update fields if provided
      if (args.title !== undefined) {
        todo.title = args.title;
      }
      if (args.completed !== undefined) {
        todo.completed = args.completed;
      }
      
      return todo;
    },
    
    // Delete todo
    deleteTodo: (parent, args) => {
      const index = todos.findIndex(t => t.id === args.id);
      
      if (index === -1) {
        return {
          success: false,
          message: `Todo with ID ${args.id} not found`
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
```

---

## Day 8: Advanced Schema Design

### Input Types

Instead of multiple arguments, use input types for cleaner mutations.

**Schema:**
```graphql
input CreateTodoInput {
  title: String!
  description: String
}

input UpdateTodoInput {
  title: String
  description: String
  completed: Boolean
}

type Mutation {
  createTodo(input: CreateTodoInput!): Todo!
  updateTodo(id: ID!, input: UpdateTodoInput!): Todo!
}
```

**Resolver:**
```javascript
createTodo: (parent, { input }) => {
  const newTodo = {
    id: getNextId(),
    title: input.title,
    description: input.description || '',
    completed: false,
    createdAt: new Date().toISOString()
  };
  
  todos.push(newTodo);
  return newTodo;
}
```

### Enums

Define a fixed set of values.

**Schema:**
```graphql
enum TodoStatus {
  ACTIVE
  COMPLETED
  ARCHIVED
}

type Todo {
  id: ID!
  title: String!
  status: TodoStatus!
}

type Query {
  todosByStatus(status: TodoStatus!): [Todo!]!
}
```

**Resolver:**
```javascript
todosByStatus: (parent, { status }) => {
  return todos.filter(todo => todo.status === status);
}
```

### Relationships Between Types

**Schema with Relations:**
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  todos: [Todo!]!
}

type Todo {
  id: ID!
  title: String!
  completed: Boolean!
  author: User!
}

type Query {
  user(id: ID!): User
  users: [User!]!
  todos: [Todo!]!
}
```

**Data:**
```javascript
const users = [
  { id: '1', name: 'Alice', email: 'alice@example.com' },
  { id: '2', name: 'Bob', email: 'bob@example.com' }
];

const todos = [
  { id: '1', title: 'Task 1', completed: false, authorId: '1' },
  { id: '2', title: 'Task 2', completed: true, authorId: '1' },
  { id: '3', title: 'Task 3', completed: false, authorId: '2' }
];
```

**Resolvers with Relations:**
```javascript
const resolvers = {
  Query: {
    users: () => users,
    user: (parent, { id }) => users.find(u => u.id === id),
    todos: () => todos
  },
  
  // Field-level resolvers
  User: {
    // Resolve todos for a user
    todos: (parent) => {
      // parent is the User object
      return todos.filter(todo => todo.authorId === parent.id);
    }
  },
  
  Todo: {
    // Resolve author for a todo
    author: (parent) => {
      // parent is the Todo object
      return users.find(user => user.id === parent.authorId);
    }
  }
};
```

**Query Example:**
```graphql
query {
  users {
    name
    todos {
      title
      completed
    }
  }
}
```

---

## Day 9: Context and Error Handling

### Using Context

Context is shared across all resolvers - perfect for authentication, database connections, etc.

**Setup:**
```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    // This runs for every request
    return {
      user: null, // Add auth user here
      db: { users, todos }, // Share data access
      utils: {
        getNextId
      }
    };
  }
});
```

**Using in Resolvers:**
```javascript
const resolvers = {
  Query: {
    todos: (parent, args, context) => {
      // Access data from context
      return context.db.todos;
    }
  },
  
  Mutation: {
    createTodo: (parent, { input }, context) => {
      const newTodo = {
        id: context.utils.getNextId(),
        ...input,
        createdAt: new Date().toISOString()
      };
      
      context.db.todos.push(newTodo);
      return newTodo;
    }
  }
};
```

### Error Handling

**Basic Error:**
```javascript
todo: (parent, { id }, context) => {
  const todo = context.db.todos.find(t => t.id === id);
  
  if (!todo) {
    throw new Error('Todo not found');
  }
  
  return todo;
}
```

**Custom Errors with Extensions:**
```javascript
const { GraphQLError } = require('graphql');

todo: (parent, { id }, context) => {
  const todo = context.db.todos.find(t => t.id === id);
  
  if (!todo) {
    throw new GraphQLError('Todo not found', {
      extensions: {
        code: 'TODO_NOT_FOUND',
        todoId: id
      }
    });
  }
  
  return todo;
}
```

**Apollo Server Error Classes:**
```javascript
const {
  ApolloServer,
  UserInputError,
  AuthenticationError,
  ForbiddenError
} = require('apollo-server');

createTodo: (parent, { input }, context) => {
  if (!input.title || input.title.trim().length === 0) {
    throw new UserInputError('Title cannot be empty', {
      invalidArgs: ['title']
    });
  }
  
  // ... create todo
}
```

---

## Day 10: Best Practices and Testing

### Project Structure

```
my-graphql-server/
├── src/
│   ├── schema/
│   │   ├── typeDefs.js
│   │   └── resolvers.js
│   ├── models/
│   │   ├── User.js
│   │   └── Todo.js
│   ├── data/
│   │   └── index.js
│   └── server.js
├── package.json
└── README.md
```

### Modular Schema

**schema/typeDefs.js:**
```javascript
const { gql } = require('apollo-server');

const typeDefs = gql`
  type Todo {
    id: ID!
    title: String!
    completed: Boolean!
    author: User!
  }

  type User {
    id: ID!
    name: String!
    todos: [Todo!]!
  }

  type Query {
    todos: [Todo!]!
    users: [User!]!
  }

  type Mutation {
    createTodo(title: String!): Todo!
  }
`;

module.exports = typeDefs;
```

**schema/resolvers.js:**
```javascript
const resolvers = {
  Query: {
    todos: (parent, args, context) => context.db.todos,
    users: (parent, args, context) => context.db.users
  },
  
  Mutation: {
    createTodo: (parent, { title }, context) => {
      // implementation
    }
  },
  
  User: {
    todos: (parent, args, context) => {
      return context.db.todos.filter(t => t.authorId === parent.id);
    }
  },
  
  Todo: {
    author: (parent, args, context) => {
      return context.db.users.find(u => u.id === parent.authorId);
    }
  }
};

module.exports = resolvers;
```

### Manual Testing

**Using curl:**
```bash
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ todos { id title } }"}'
```

**Testing Mutations:**
```bash
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createTodo(title: \"New Task\") { id title } }"
  }'
```

---

## Complete Example: Blog API

Here's a complete blog API to study:

```javascript
const { ApolloServer, gql, UserInputError } = require('apollo-server');

// Schema
const typeDefs = gql`
  type Post {
    id: ID!
    title: String!
    content: String!
    published: Boolean!
    author: User!
    comments: [Comment!]!
  }

  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Comment {
    id: ID!
    text: String!
    post: Post!
    author: User!
  }

  type Query {
    posts: [Post!]!
    post(id: ID!): Post
    users: [User!]!
    user(id: ID!): User
  }

  type Mutation {
    createPost(title: String!, content: String!, authorId: ID!): Post!
    publishPost(id: ID!): Post!
    createComment(postId: ID!, authorId: ID!, text: String!): Comment!
  }
`;

// In-memory data
let posts = [];
let users = [
  { id: '1', name: 'Alice', email: 'alice@example.com' },
  { id: '2', name: 'Bob', email: 'bob@example.com' }
];
let comments = [];
let nextPostId = 1;
let nextCommentId = 1;

// Resolvers
const resolvers = {
  Query: {
    posts: () => posts,
    post: (_, { id }) => posts.find(p => p.id === id),
    users: () => users,
    user: (_, { id }) => users.find(u => u.id === id)
  },

  Mutation: {
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
      const comment = {
        id: String(nextCommentId++),
        text,
        postId,
        authorId
      };

      comments.push(comment);
      return comment;
    }
  },

  Post: {
    author: (parent) => users.find(u => u.id === parent.authorId),
    comments: (parent) => comments.filter(c => c.postId === parent.id)
  },

  User: {
    posts: (parent) => posts.filter(p => p.authorId === parent.id)
  },

  Comment: {
    post: (parent) => posts.find(p => p.id === parent.postId),
    author: (parent) => users.find(u => u.id === parent.authorId)
  }
};

// Server
const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
```

---

## Checklist: What You Should Know

After completing Phase 3, you should be able to:

- [ ] Set up a GraphQL server with Apollo Server
- [ ] Define schemas using SDL
- [ ] Implement query resolvers
- [ ] Implement mutation resolvers
- [ ] Handle relationships between types
- [ ] Use context for shared data
- [ ] Implement basic error handling
- [ ] Structure a GraphQL project
- [ ] Test your API manually

---

## Next Steps

Ready for Phase 4?
- Connect to a real database
- Implement authentication
- Add DataLoader for performance
- Build production-ready features

**Congratulations!** You've built your first GraphQL server!
