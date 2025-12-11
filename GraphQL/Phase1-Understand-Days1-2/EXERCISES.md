# Phase 1: Terminal Exercises (Days 1-2)

These exercises help you explore GraphQL concepts using your Linux terminal.

---

## Exercise 1: Install GraphQL Tools

**Goal**: Set up tools to interact with GraphQL APIs from the terminal.

### Step 1: Install Node.js and npm (if not already installed)
```bash
# Check if Node.js is installed
node --version

# Check if npm is installed
npm --version

# If not installed, install Node.js (includes npm)
# For Ubuntu/Debian:
sudo apt update
sudo apt install nodejs npm -y

# Verify installation
node --version && npm --version
```

### Step 2: Install GraphQL CLI tools globally
```bash
# Install graphqurl - a curl-like CLI for GraphQL
npm install -g graphqurl

# Verify installation
gql --version
```

**Expected Output**: Version number of graphqurl

---

## Exercise 2: Query a Public GraphQL API

**Goal**: Make your first GraphQL query from the terminal.

### Using the Countries API

```bash
# Simple query to get all country codes and names
gql https://countries.trevorblades.com/ \
  -q 'query { countries { code name } }'
```

**Expected Output**: JSON response with array of countries

### Try These Variations:

```bash
# Get more fields
gql https://countries.trevorblades.com/ \
  -q 'query { countries { code name capital currency } }'

# Get a specific country (using variables)
gql https://countries.trevorblades.com/ \
  -q 'query($code: ID!) { country(code: $code) { name capital currency } }' \
  -v '{"code": "US"}'

# Get country with its continent
gql https://countries.trevorblades.com/ \
  -q 'query { country(code: "KE") { name continent { name } languages { name } } }'
```

**Tasks**:
1. Query for Kenya (KE) and get its name, capital, and languages
2. Query for your country and explore all available fields
3. Get all continents and their codes

---

## Exercise 3: Explore Schema Using Introspection

**Goal**: Learn to discover what's available in a GraphQL API.

### Get the Schema
```bash
# Get the full schema documentation
gql https://countries.trevorblades.com/ --introspect > schema.json

# View the schema
cat schema.json | jq '.' | less
```

### Query for Available Types
```bash
# Get all type names
gql https://countries.trevorblades.com/ \
  -q '{ __schema { types { name kind } } }' | jq '.data.__schema.types[] | select(.kind == "OBJECT") | .name'

# Get details about a specific type
gql https://countries.trevorblades.com/ \
  -q '{ __type(name: "Country") { name fields { name type { name kind } } } }' | jq '.'
```

**Tasks**:
1. List all available types in the Countries API
2. Explore the fields available on the `Country` type
3. Find out what the `Query` root type offers

---

## Exercise 4: Use curl with GraphQL

**Goal**: Understand that GraphQL is just HTTP POST requests.

### Basic curl Request
```bash
# POST a GraphQL query using curl
curl -X POST https://countries.trevorblades.com/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ countries { code name } }"}' | jq '.'
```

### With Variables
```bash
# Query with variables
curl -X POST https://countries.trevorblades.com/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query($code: ID!) { country(code: $code) { name capital } }",
    "variables": {"code": "US"}
  }' | jq '.'
```

**Tasks**:
1. Use curl to query for all continents
2. Use curl with variables to get information about 3 different countries
3. Format the output using `jq` to show only the country names

---

## Exercise 5: Compare REST vs GraphQL

**Goal**: See the practical difference between REST and GraphQL.

### REST API Example
```bash
# With REST, you often get all fields
curl https://jsonplaceholder.typicode.com/users/1 | jq '.'

# You can't select specific fields - you get everything
```

### GraphQL Example
```bash
# With GraphQL, you choose exactly what you need
gql https://countries.trevorblades.com/ \
  -q 'query { country(code: "US") { name } }'

# vs getting more fields
gql https://countries.trevorblades.com/ \
  -q 'query { country(code: "US") { name capital currency phone languages { name } } }'
```

**Tasks**:
1. Use a REST API to fetch user data - notice you get all fields
2. Use GraphQL to fetch only 2 fields from a country
3. Compare the response sizes (use `wc -c` to count bytes)

```bash
# Count bytes in REST response
curl -s https://jsonplaceholder.typicode.com/users/1 | wc -c

# Count bytes in GraphQL response (minimal fields)
gql https://countries.trevorblades.com/ \
  -q 'query { country(code: "US") { name } }' | wc -c
```

---

## Exercise 6: Practice with SpaceX API

**Goal**: Work with a more complex GraphQL API.

### Explore SpaceX Launches
```bash
# Get latest 5 launches
gql https://api.spacex.land/graphql/ \
  -q 'query { launchesPast(limit: 5) { mission_name launch_date_local } }'

# Get detailed information about a specific launch
gql https://api.spacex.land/graphql/ \
  -q 'query { 
    launchesPast(limit: 1) { 
      mission_name 
      launch_date_local 
      rocket { 
        rocket_name 
        rocket_type 
      } 
      ships { 
        name 
        home_port 
      } 
    } 
  }'
```

### Explore Ships
```bash
# Get all ships
gql https://api.spacex.land/graphql/ \
  -q 'query { ships(limit: 10) { name type year_built } }'
```

**Tasks**:
1. Get the last 10 SpaceX launches with mission names and dates
2. Find information about a specific rocket (Falcon 9)
3. Explore the schema to find what other data is available

---

## Exercise 7: Create a Script to Query Multiple APIs

**Goal**: Automate GraphQL queries using shell scripts.

### Create a Shell Script
```bash
# Create a script file
cat > graphql-explorer.sh << 'EOF'
#!/bin/bash

echo "=== Countries API ==="
gql https://countries.trevorblades.com/ \
  -q 'query { countries(filter: {code: {in: ["US", "KE", "GB"]}}) { code name capital } }'

echo ""
echo "=== SpaceX API ==="
gql https://api.spacex.land/graphql/ \
  -q 'query { launchesPast(limit: 3) { mission_name launch_date_local } }'

echo ""
echo "Done!"
EOF

# Make it executable
chmod +x graphql-explorer.sh

# Run it
./graphql-explorer.sh
```

**Tasks**:
1. Modify the script to query your favorite countries
2. Add another API call to get SpaceX rocket information
3. Format the output to be more readable

---

## Exercise 8: Understanding Query Structure

**Goal**: Learn to read and write GraphQL query syntax.

### Save Queries to Files
```bash
# Create a query file
cat > country-query.graphql << 'EOF'
query GetCountryDetails($code: ID!) {
  country(code: $code) {
    code
    name
    capital
    currency
    languages {
      code
      name
    }
    continent {
      name
    }
  }
}
EOF

# Create a variables file
cat > variables.json << 'EOF'
{
  "code": "KE"
}
EOF

# Execute the query
gql https://countries.trevorblades.com/ \
  --queryFile country-query.graphql \
  --variablesFile variables.json
```

**Tasks**:
1. Create a query file for getting continent information
2. Create a variables file with different country codes
3. Execute the query with different variables

---

## Exercise 9: Analyze GraphQL Responses

**Goal**: Parse and analyze GraphQL responses using jq.

### Extract Specific Data
```bash
# Get only country names
gql https://countries.trevorblades.com/ \
  -q 'query { countries { name } }' | \
  jq -r '.data.countries[].name' | head -10

# Count total countries
gql https://countries.trevorblades.com/ \
  -q 'query { countries { name } }' | \
  jq '.data.countries | length'

# Filter countries by name pattern
gql https://countries.trevorblades.com/ \
  -q 'query { countries { name capital } }' | \
  jq '.data.countries[] | select(.name | contains("United"))'
```

**Tasks**:
1. Extract all country names starting with "A"
2. Count how many countries have a capital defined
3. Create a CSV file with country codes and names

```bash
# Create CSV
gql https://countries.trevorblades.com/ \
  -q 'query { countries { code name } }' | \
  jq -r '.data.countries[] | [.code, .name] | @csv' > countries.csv

# View the CSV
head -20 countries.csv
```

---

## Exercise 10: Error Handling and Debugging

**Goal**: Understand GraphQL errors and how to debug them.

### Trigger Intentional Errors
```bash
# Invalid field name
gql https://countries.trevorblades.com/ \
  -q 'query { countries { invalidField } }'

# Wrong variable type
gql https://countries.trevorblades.com/ \
  -q 'query($code: String!) { country(code: $code) { name } }' \
  -v '{"code": 123}'

# Missing required variable
gql https://countries.trevorblades.com/ \
  -q 'query($code: ID!) { country(code: $code) { name } }'
```

**Observe**:
- How GraphQL returns errors in the response
- Error messages are descriptive
- You get the exact location of the error

---

## Bonus Exercise: Create a GraphQL Query Tester

**Goal**: Build a reusable tool for testing queries.

```bash
# Create an advanced testing script
cat > graphql-tester.sh << 'EOF'
#!/bin/bash

API_URL=$1
QUERY=$2

if [ -z "$API_URL" ] || [ -z "$QUERY" ]; then
    echo "Usage: $0 <api-url> <query>"
    echo "Example: $0 https://countries.trevorblades.com/ '{ countries { name } }'"
    exit 1
fi

echo "Testing GraphQL API: $API_URL"
echo "Query: $QUERY"
echo "---"

RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$QUERY\"}")

# Check if there are errors
ERRORS=$(echo "$RESPONSE" | jq -r '.errors')

if [ "$ERRORS" != "null" ]; then
    echo "❌ Query failed with errors:"
    echo "$ERRORS" | jq '.'
    exit 1
else
    echo "✅ Query successful!"
    echo "$RESPONSE" | jq '.data'
fi
EOF

chmod +x graphql-tester.sh

# Test it
./graphql-tester.sh https://countries.trevorblades.com/ '{ countries { code name } }'
```

---

## Challenge Exercises

Ready for more? Try these:

1. **Schema Explorer**: Write a script that takes a GraphQL endpoint and lists all available queries

2. **Query Builder**: Create an interactive script that helps build GraphQL queries

3. **API Comparison**: Query multiple GraphQL APIs and compare their response times

4. **Data Formatter**: Create a script that converts GraphQL responses to different formats (CSV, Markdown table, etc.)

---

## Verification Checklist

After completing these exercises, you should be able to:

- [ ] Query a GraphQL API using `graphqurl` (gql command)
- [ ] Query a GraphQL API using curl
- [ ] Use variables in GraphQL queries
- [ ] Introspect a GraphQL schema
- [ ] Parse GraphQL responses with jq
- [ ] Create shell scripts for GraphQL queries
- [ ] Debug GraphQL errors
- [ ] Compare REST and GraphQL in practice

---

## Useful Commands Reference

```bash
# Query with graphqurl
gql <endpoint> -q '<query>'

# Query with variables
gql <endpoint> -q '<query>' -v '<variables-json>'

# Introspect schema
gql <endpoint> --introspect

# Query with curl
curl -X POST <endpoint> \
  -H "Content-Type: application/json" \
  -d '{"query": "<query>"}'

# Pretty print JSON with jq
... | jq '.'

# Extract specific fields with jq
... | jq '.data.countries[].name'

# Count items
... | jq '.data.countries | length'
```

---

## Next Steps

Once you're comfortable with these terminal exercises:
1. Move to Phase 2 exercises to practice writing complex queries
2. Experiment with different public GraphQL APIs
3. Try combining multiple queries in shell scripts

**Remember**: The terminal is a powerful way to explore and test GraphQL APIs!
