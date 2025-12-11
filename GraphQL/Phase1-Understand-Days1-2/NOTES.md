# Phase 1: Understand GraphQL (Days 1-2)

## Learning Objectives
By the end of this phase, you should:
- Understand what GraphQL is and why it exists
- Grasp the fundamental differences between GraphQL and REST
- Understand the GraphQL type system and Schema Definition Language (SDL)
- Be able to read and understand basic GraphQL schemas
- Know how to use GraphQL playgrounds/explorers

---

## Day 1: Core Concepts

### What is GraphQL?

GraphQL is a **query language for APIs** and a runtime for executing those queries. Think of it as a more flexible alternative to REST APIs.

**Key Characteristics:**
- **Single Endpoint**: Unlike REST with multiple endpoints (`/users`, `/posts`), GraphQL uses one endpoint (typically `/graphql`)
- **Client-Specified Queries**: Clients ask for exactly what they need
- **Strongly Typed**: Every piece of data has a defined type
- **Hierarchical**: Queries mirror the shape of the data returned

### Why GraphQL Over REST?

| Problem with REST | GraphQL Solution |
|-------------------|------------------|
| **Over-fetching**: Get entire user object when you only need the name | Request only the fields you need |
| **Under-fetching**: Need multiple requests for related data | Get everything in one request |
| **API Versioning**: Breaking changes require `/v2/` endpoints | Add new fields without breaking old queries |
| **Documentation**: Often out of sync | Self-documenting through introspection |

**Real-World Example:**

REST Approach:
```
GET /users/123        → Returns: { id, name, email, age, address, phone, ... }
GET /users/123/posts  → Returns: [{ id, title, content, ... }, ...]
GET /posts/456/comments → Returns: [{ id, text, ... }, ...]
```
Result: 3 requests, lots of unused data

GraphQL Approach:
```graphql
{
  user(id: "123") {
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
Result: 1 request, exactly what you need

### The Type System

GraphQL uses a **strongly-typed schema** that defines:
1. What data is available
2. What operations can be performed
3. The relationships between data

**Built-in Scalar Types:**
- `Int`: Signed 32-bit integer
- `Float`: Signed double-precision floating-point
- `String`: UTF-8 character sequence
- `Boolean`: true or false
- `ID`: Unique identifier (serialized as String)

**Type Modifiers:**
- `!` (Non-null): Field must always have a value
  - `String!` → required string
  - `String` → optional string (can be null)
- `[]` (List): Field is an array
  - `[String]` → array of strings (array can be null, items can be null)
  - `[String!]!` → non-null array of non-null strings

### Schema Definition Language (SDL)

SDL is the syntax for defining your GraphQL schema.

**Basic Type Definition:**
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  isActive: Boolean!
}
```

**Understanding the Syntax:**
- `type User`: Define a new object type called User
- `id: ID!`: Field named `id` of type `ID`, required (!)
- `age: Int`: Optional integer field (no !)

**Root Operation Types:**

Every GraphQL schema must have at least a `Query` type:

```graphql
type Query {
  hello: String
  user(id: ID!): User
  users: [User!]!
}
```

This defines three possible queries:
1. `hello`: Returns an optional string
2. `user(id: ID!)`: Takes a required ID argument, returns a User or null
3. `users`: Returns a non-null array of non-null Users

**Relationships Between Types:**
```graphql
type User {
  id: ID!
  name: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}
```

This creates a bidirectional relationship:
- User has many Posts
- Post belongs to one User

---

## Day 2: Exploring GraphQL in Practice

### Using GraphQL Playgrounds

**GraphiQL**: Web-based IDE that comes with most GraphQL servers
- Auto-completion as you type
- Documentation explorer
- Query history
- Syntax highlighting

**Apollo Studio Explorer**: Modern cloud-based playground
- URL: https://studio.apollographql.com/sandbox/explorer
- Supports any public GraphQL endpoint
- Visual query builder
- Response caching

### Public APIs to Practice With

1. **Countries API** (Easiest)
   - Endpoint: `https://countries.trevorblades.com/`
   - Great for beginners
   - Simple schema with countries, continents, languages

2. **SpaceX API**
   - Endpoint: `https://api.spacex.land/graphql/`
   - Real SpaceX data (launches, rockets, missions)
   - More complex relationships

3. **GitHub GraphQL API**
   - Endpoint: `https://api.github.com/graphql`
   - Requires authentication
   - Production-quality API

### Reading a GraphQL Schema

When you open a GraphQL playground, look for the "Docs" or "Schema" tab.

**What to Look For:**

1. **Root Types**: Start here
   ```graphql
   type Query {
     ...
   }
   type Mutation {
     ...
   }
   ```

2. **Available Queries**: What data can you fetch?
   ```graphql
   type Query {
     countries: [Country!]!
     country(code: ID!): Country
   }
   ```

3. **Type Definitions**: What fields are available?
   ```graphql
   type Country {
     code: ID!
     name: String!
     continent: Continent!
     languages: [Language!]!
   }
   ```

4. **Arguments**: What parameters can you pass?
   ```graphql
   user(id: ID!): User
   posts(limit: Int, offset: Int): [Post!]!
   ```

### Key Concepts to Master

**1. Non-Null vs Nullable**
```graphql
type User {
  name: String!   # Always present
  age: Int        # Can be null
}
```

**2. Lists and Their Nullability**
```graphql
type Query {
  users: [User]       # Array can be null, items can be null
  users: [User]!      # Array cannot be null, but items can
  users: [User!]!     # Array cannot be null, items cannot be null
}
```

**3. Input Types** (for mutations)
```graphql
input CreateUserInput {
  name: String!
  email: String!
  age: Int
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}
```

**4. Enums** (predefined set of values)
```graphql
enum Role {
  ADMIN
  USER
  GUEST
}

type User {
  id: ID!
  role: Role!
}
```

**5. Interfaces** (shared fields across types)
```graphql
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
}

type Post implements Node {
  id: ID!
  title: String!
}
```

### Common Patterns to Recognize

**1. Pagination Pattern:**
```graphql
type Query {
  users(first: Int, after: String): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

**2. Mutation Response Pattern:**
```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

---

## Checklist: What You Should Know

After completing Phase 1, you should be able to:

- [ ] Explain what GraphQL is in one sentence
- [ ] List 3 advantages of GraphQL over REST
- [ ] Identify the 5 scalar types in GraphQL
- [ ] Understand the difference between `String` and `String!`
- [ ] Read a GraphQL schema and understand what queries are available
- [ ] Open a GraphQL playground and explore the documentation
- [ ] Recognize common patterns (pagination, mutations, relationships)

---

## Quick Reference

### Type System Cheat Sheet
```graphql
# Scalar Types
Int, Float, String, Boolean, ID

# Non-null
String!  # Required
String   # Optional

# Lists
[String]      # Nullable array of nullable strings
[String!]     # Nullable array of non-null strings
[String]!     # Non-null array of nullable strings
[String!]!    # Non-null array of non-null strings

# Custom Types
type TypeName {
  field: Type
}

# Input Types (for mutations)
input InputName {
  field: Type
}

# Enums
enum EnumName {
  VALUE1
  VALUE2
}

# Root Types
type Query { ... }      # Required
type Mutation { ... }   # Optional
type Subscription { ... } # Optional
```

---

## Next Steps

Once you're comfortable with these concepts:
1. Move to Phase 2 to learn how to write queries and mutations
2. Practice exploring different public GraphQL APIs
3. Try to understand the schema before writing any queries

**Remember**: Understanding the schema is 80% of using GraphQL effectively!
