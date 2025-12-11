# Phase 2: Consume GraphQL APIs (Days 3-5)

## Learning Objectives
By the end of this phase, you should:
- Write complex GraphQL queries with nested fields
- Use arguments, aliases, and fragments effectively
- Understand and write mutations
- Work with variables in queries and mutations
- Use GraphQL playgrounds effectively
- Understand best practices for consuming GraphQL APIs

---

## Day 3: Advanced Queries

### Nested Queries

One of GraphQL's superpowers is fetching related data in a single request.

**Example Schema:**
```graphql
type User {
  id: ID!
  name: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  author: User!
  comments: [Comment!]!
}

type Comment {
  id: ID!
  text: String!
  author: User!
}
```

**Nested Query:**
```graphql
query {
  user(id: "1") {
    name
    posts {
      title
      comments {
        text
        author {
          name
        }
      }
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "user": {
      "name": "Alice",
      "posts": [
        {
          "title": "GraphQL Basics",
          "comments": [
            {
              "text": "Great post!",
              "author": { "name": "Bob" }
            }
          ]
        }
      ]
    }
  }
}
```

### Arguments in Queries

Arguments allow you to filter, sort, and paginate data.

**Common Argument Patterns:**

**1. Filtering:**
```graphql
query {
  posts(status: PUBLISHED, category: "tech") {
    title
  }
}
```

**2. Sorting:**
```graphql
query {
  posts(sortBy: DATE, order: DESC) {
    title
    publishedAt
  }
}
```

**3. Pagination:**
```graphql
query {
  posts(limit: 10, offset: 0) {
    title
  }
}
```

**4. Search:**
```graphql
query {
  searchPosts(query: "GraphQL", first: 5) {
    title
    excerpt
  }
}
```

**Multiple Arguments:**
```graphql
query {
  users(
    role: ADMIN,
    active: true,
    limit: 10,
    sortBy: CREATED_AT
  ) {
    id
    name
    role
  }
}
```

### Aliases

Aliases let you rename fields in the response, useful when querying the same field multiple times with different arguments.

**Without Aliases (Error - duplicate fields):**
```graphql
query {
  user(id: "1") { name }
  user(id: "2") { name }  # ❌ Can't have duplicate keys
}
```

**With Aliases (Correct):**
```graphql
query {
  firstUser: user(id: "1") {
    name
    email
  }
  secondUser: user(id: "2") {
    name
    email
  }
}
```

**Response:**
```json
{
  "data": {
    "firstUser": { "name": "Alice", "email": "alice@example.com" },
    "secondUser": { "name": "Bob", "email": "bob@example.com" }
  }
}
```

**Practical Example - Comparing Data:**
```graphql
query {
  popularPosts: posts(sortBy: VIEWS, limit: 5) {
    title
    views
  }
  recentPosts: posts(sortBy: DATE, limit: 5) {
    title
    publishedAt
  }
  myPosts: posts(authorId: "123") {
    title
    status
  }
}
```

### Fragments

Fragments are reusable units of query logic.

**Basic Fragment:**
```graphql
fragment UserBasicInfo on User {
  id
  name
  email
  avatar
}

query {
  user(id: "1") {
    ...UserBasicInfo
    createdAt
  }
  currentUser {
    ...UserBasicInfo
    lastLogin
  }
}
```

**Nested Fragments:**
```graphql
fragment UserInfo on User {
  id
  name
  avatar
}

fragment PostInfo on Post {
  id
  title
  author {
    ...UserInfo
  }
}

query {
  posts {
    ...PostInfo
    comments {
      text
      author {
        ...UserInfo
      }
    }
  }
}
```

**When to Use Fragments:**
1. Repeated field selections
2. Shared data requirements across components
3. Organizing complex queries
4. Creating reusable query building blocks

---

## Day 4: Variables and Mutations

### Query Variables

Variables make queries reusable and safer (prevents injection attacks).

**Query with Inline Arguments (Bad Practice):**
```graphql
query {
  user(id: "123") {
    name
  }
}
```

**Query with Variables (Best Practice):**
```graphql
query GetUser($userId: ID!) {
  user(id: $userId) {
    name
    email
  }
}
```

**Variables (sent separately):**
```json
{
  "userId": "123"
}
```

**Variable Types:**
```graphql
# Required variable
query($id: ID!) { ... }

# Optional variable
query($id: ID) { ... }

# Variable with default value
query($limit: Int = 10) { ... }

# List variable
query($ids: [ID!]!) { ... }

# Input type variable
query($input: CreateUserInput!) { ... }
```

**Multiple Variables:**
```graphql
query GetPosts(
  $limit: Int = 10,
  $offset: Int = 0,
  $status: PostStatus!,
  $authorId: ID
) {
  posts(
    limit: $limit,
    offset: $offset,
    status: $status,
    authorId: $authorId
  ) {
    id
    title
    status
  }
}
```

### Understanding Mutations

Mutations are for creating, updating, or deleting data.

**Basic Mutation Structure:**
```graphql
mutation OperationName($variable: Type!) {
  mutationField(argument: $variable) {
    # Return fields
    id
    field1
    field2
  }
}
```

**Create Mutation:**
```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
    createdAt
  }
}
```

**Variables:**
```json
{
  "input": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
}
```

**Update Mutation:**
```graphql
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    email
    updatedAt
  }
}
```

**Delete Mutation:**
```graphql
mutation DeleteUser($id: ID!) {
  deleteUser(id: $id) {
    success
    message
  }
}
```

### Mutation Best Practices

**1. Always Return Useful Data:**
```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id              # Get the new ID
    title
    slug            # Get computed values
    publishedAt
    author {        # Get related data
      name
    }
  }
}
```

**2. Use Input Types:**
```graphql
# Define input type in schema
input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
  published: Boolean
}

# Use in mutation
mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
  }
}
```

**3. Return Error Information:**
```graphql
type CreateUserPayload {
  user: User
  errors: [UserError!]
}

type UserError {
  field: String!
  message: String!
}

mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
    }
    errors {
      field
      message
    }
  }
}
```

### Multiple Mutations (Sequential Execution)

Unlike queries (which execute in parallel), mutations execute sequentially.

```graphql
mutation CreatePostWithComment {
  # 1. Create post (executes first)
  createPost(input: {
    title: "New Post"
    content: "Content here"
  }) {
    id
    title
  }
  
  # 2. Create comment (executes second)
  createComment(input: {
    postId: "generated-id-from-above"
    text: "First comment!"
  }) {
    id
    text
  }
}
```

---

## Day 5: Advanced Patterns

### Conditional Fields with Directives

GraphQL provides built-in directives for conditional logic.

**@include Directive:**
```graphql
query GetUser($includeEmail: Boolean!) {
  user(id: "1") {
    name
    email @include(if: $includeEmail)
  }
}
```

**@skip Directive:**
```graphql
query GetUser($skipEmail: Boolean!) {
  user(id: "1") {
    name
    email @skip(if: $skipEmail)
  }
}
```

**Variables:**
```json
{
  "includeEmail": true,
  "skipEmail": false
}
```

### Named Queries and Mutations

Give your operations descriptive names.

**Bad (Anonymous):**
```graphql
query {
  users { name }
}
```

**Good (Named):**
```graphql
query GetAllActiveUsers {
  users(active: true) {
    name
    email
  }
}
```

**Benefits:**
- Better debugging
- Server-side logging
- Client-side cache management
- Documentation

### Optimistic Updates Pattern

When using mutations, return enough data to update your cache.

```graphql
mutation LikePost($postId: ID!) {
  likePost(postId: $postId) {
    post {
      id
      likeCount        # Updated count
      isLikedByMe      # Updated state
    }
  }
}
```

### Pagination Patterns

**Limit/Offset Pattern (Simple):**
```graphql
query GetPosts($limit: Int!, $offset: Int!) {
  posts(limit: $limit, offset: $offset) {
    id
    title
  }
}
```

**Cursor-Based Pattern (Recommended):**
```graphql
query GetPosts($first: Int!, $after: String) {
  posts(first: $first, after: $after) {
    edges {
      cursor
      node {
        id
        title
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Error Handling

GraphQL responses can contain both data and errors.

**Successful Response:**
```json
{
  "data": {
    "user": { "name": "Alice" }
  }
}
```

**Error Response:**
```json
{
  "errors": [
    {
      "message": "User not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["user"],
      "extensions": {
        "code": "USER_NOT_FOUND"
      }
    }
  ],
  "data": {
    "user": null
  }
}
```

**Partial Success:**
```json
{
  "data": {
    "user": { "name": "Alice" },
    "posts": null
  },
  "errors": [
    {
      "message": "Failed to fetch posts",
      "path": ["posts"]
    }
  ]
}
```

---

## Best Practices Summary

### Query Best Practices

1. **Always Use Variables** - Never inline user input
2. **Name Your Operations** - Helps with debugging
3. **Request Only What You Need** - Avoid over-fetching
4. **Use Fragments** - DRY (Don't Repeat Yourself)
5. **Use Aliases** - When querying the same field multiple times

### Mutation Best Practices

1. **Return Modified Data** - Include updated fields
2. **Use Input Types** - Group related arguments
3. **Include Error Handling** - Return errors explicitly
4. **Be Idempotent** - Same mutation = same result (when possible)
5. **Return IDs** - Always return created IDs

### Performance Best Practices

1. **Limit Depth** - Don't nest too deeply
2. **Use Pagination** - For large lists
3. **Request Only Needed Fields** - Smaller payloads
4. **Batch Queries** - Combine multiple queries when possible

---

## Common Patterns Cheat Sheet

### Basic Query
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}
```

### Query with Nested Data
```graphql
query GetUserWithPosts($id: ID!) {
  user(id: $id) {
    name
    posts {
      title
      comments {
        text
      }
    }
  }
}
```

### Query with Fragments
```graphql
fragment UserFields on User {
  id
  name
  email
}

query {
  user1: user(id: "1") { ...UserFields }
  user2: user(id: "2") { ...UserFields }
}
```

### Create Mutation
```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
```

### Update Mutation
```graphql
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    updatedAt
  }
}
```

### Delete Mutation
```graphql
mutation DeleteUser($id: ID!) {
  deleteUser(id: $id) {
    success
    message
  }
}
```

---

## Checklist: What You Should Know

After completing Phase 2, you should be able to:

- [ ] Write nested queries to fetch related data
- [ ] Use arguments to filter and sort data
- [ ] Use aliases to rename fields
- [ ] Create and use fragments
- [ ] Write queries with variables
- [ ] Write create, update, and delete mutations
- [ ] Handle errors in GraphQL responses
- [ ] Understand pagination patterns
- [ ] Use directives like @include and @skip
- [ ] Follow GraphQL best practices

---

## Next Steps

Ready for Phase 3?
1. You'll build your first GraphQL server
2. Define your own schema
3. Implement resolvers
4. Handle real data

**Tip**: Keep practicing with public APIs before moving to building your own!
