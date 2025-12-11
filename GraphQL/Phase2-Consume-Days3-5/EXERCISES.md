# Phase 2: Terminal Exercises (Days 3-5)

Practice writing advanced queries and mutations using the terminal.

---

## Exercise 1: Nested Queries Practice

**Goal**: Master querying related data in a single request.

### Countries API - Nested Data
```bash
# Get country with continent and languages
gql https://countries.trevorblades.com/ \
  -q 'query {
    country(code: "US") {
      name
      capital
      continent {
        name
        countries {
          name
        }
      }
      languages {
        code
        name
      }
    }
  }'
```

### SpaceX API - Complex Nesting
```bash
# Get launches with rocket and ship details
gql https://api.spacex.land/graphql/ \
  -q 'query {
    launchesPast(limit: 3) {
      mission_name
      launch_date_local
      rocket {
        rocket_name
        rocket_type
      }
      ships {
        name
        home_port
        image
      }
    }
  }'
```

**Tasks**:
1. Query Kenya (KE) with all its languages and continent information
2. Get the last SpaceX launch with full rocket details
3. Query a continent and list all its countries with their currencies

---

## Exercise 2: Using Arguments

**Goal**: Filter, sort, and limit query results.

### Filtering with Arguments
```bash
# Get countries by continent code
gql https://countries.trevorblades.com/ \
  -q 'query {
    countries(filter: { continent: { eq: "AF" } }) {
      code
      name
      capital
    }
  }' | jq '.data.countries | length'

# Get multiple specific countries
gql https://countries.trevorblades.com/ \
  -q 'query {
    countries(filter: { code: { in: ["US", "KE", "GB", "JP"] } }) {
      code
      name
      capital
      currency
    }
  }'
```

### SpaceX API with Limits
```bash
# Get limited number of launches
gql https://api.spacex.land/graphql/ \
  -q 'query {
    launchesPast(limit: 5, offset: 0) {
      mission_name
      launch_year
    }
  }'

# Get launches from specific year
gql https://api.spacex.land/graphql/ \
  -q 'query {
    launchesPast(find: { launch_year: "2020" }) {
      mission_name
      launch_date_local
    }
  }'
```

**Tasks**:
1. Get all countries in Europe (continent code: EU)
2. Get the first 10 SpaceX launches
3. Find SpaceX launches from 2021

---

## Exercise 3: Aliases in Action

**Goal**: Query the same field multiple times with different arguments.

### Multiple Countries with Aliases
```bash
# Compare different countries
gql https://countries.trevorblades.com/ \
  -q 'query {
    usa: country(code: "US") {
      name
      capital
      currency
    }
    kenya: country(code: "KE") {
      name
      capital
      currency
    }
    japan: country(code: "JP") {
      name
      capital
      currency
    }
  }'
```

### SpaceX Launches Comparison
```bash
# Compare different launch time periods
gql https://api.spacex.land/graphql/ \
  -q 'query {
    recent: launchesPast(limit: 5, offset: 0) {
      mission_name
      launch_year
    }
    older: launchesPast(limit: 5, offset: 10) {
      mission_name
      launch_year
    }
  }'
```

**Tasks**:
1. Create a query that compares 5 different countries side-by-side
2. Query SpaceX launches from different years using aliases
3. Compare two continents and their country counts

---

## Exercise 4: Working with Variables

**Goal**: Make reusable queries with variables.

### Create Variable-Based Query Files

```bash
# Create a country query with variables
cat > country-details.graphql << 'EOF'
query GetCountryDetails($code: ID!) {
  country(code: $code) {
    code
    name
    capital
    currency
    continent {
      name
    }
    languages {
      name
    }
  }
}
EOF

# Test with different variables
echo '{"code": "US"}' > us.json
echo '{"code": "KE"}' > kenya.json
echo '{"code": "JP"}' > japan.json

# Execute with different variables
gql https://countries.trevorblades.com/ \
  --queryFile country-details.graphql \
  --variablesFile us.json

gql https://countries.trevorblades.com/ \
  --queryFile country-details.graphql \
  --variablesFile kenya.json
```

### SpaceX Launch Query with Variables
```bash
# Create query file
cat > spacex-launches.graphql << 'EOF'
query GetLaunches($limit: Int!, $offset: Int!) {
  launchesPast(limit: $limit, offset: $offset) {
    mission_name
    launch_date_local
    rocket {
      rocket_name
    }
  }
}
EOF

# Create variables
echo '{"limit": 5, "offset": 0}' > vars-page1.json
echo '{"limit": 5, "offset": 5}' > vars-page2.json

# Execute pagination
gql https://api.spacex.land/graphql/ \
  --queryFile spacex-launches.graphql \
  --variablesFile vars-page1.json
```

**Tasks**:
1. Create a reusable query for getting continent details
2. Create a query that accepts multiple optional variables
3. Implement pagination using variables

---

## Exercise 5: Fragments Practice

**Goal**: Use fragments to avoid repetition.

### Create Fragment-Based Queries
```bash
# Query with fragments
cat > countries-with-fragments.graphql << 'EOF'
fragment CountryBasic on Country {
  code
  name
  capital
}

fragment CountryComplete on Country {
  ...CountryBasic
  currency
  phone
  continent {
    name
  }
}

query GetCountries {
  usa: country(code: "US") {
    ...CountryComplete
  }
  kenya: country(code: "KE") {
    ...CountryComplete
  }
  allCountries: countries(filter: { code: { in: ["GB", "FR", "DE"] } }) {
    ...CountryBasic
  }
}
EOF

# Execute
gql https://countries.trevorblades.com/ \
  --queryFile countries-with-fragments.graphql
```

### SpaceX with Fragments
```bash
cat > spacex-fragments.graphql << 'EOF'
fragment LaunchInfo on Launch {
  mission_name
  launch_date_local
  launch_year
}

fragment RocketInfo on LaunchRocket {
  rocket_name
  rocket_type
}

query GetDetailedLaunches {
  launchesPast(limit: 3) {
    ...LaunchInfo
    rocket {
      ...RocketInfo
    }
  }
}
EOF

gql https://api.spacex.land/graphql/ \
  --queryFile spacex-fragments.graphql
```

**Tasks**:
1. Create nested fragments (fragment within fragment)
2. Create a query using 3+ fragments
3. Reuse the same fragment in different queries

---

## Exercise 6: Simulating Mutations (Read-Only APIs)

**Goal**: Understand mutation syntax (we'll use curl with a mock API).

### Understanding Mutation Structure
```bash
# NOTE: Countries API is read-only, so we'll create mock mutations
# to understand the syntax

# Create a mutation template
cat > create-user-mutation.graphql << 'EOF'
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
    createdAt
  }
}
EOF

# Variables for the mutation
cat > create-user-vars.json << 'EOF'
{
  "input": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
}
EOF

# Show the structure (won't execute on Countries API)
echo "This is how a mutation would look:"
cat create-user-mutation.graphql
echo ""
echo "With these variables:"
cat create-user-vars.json
```

### Practice Mutation Syntax
```bash
# Create different mutation templates
cat > update-user-mutation.graphql << 'EOF'
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    email
    updatedAt
  }
}
EOF

cat > delete-user-mutation.graphql << 'EOF'
mutation DeleteUser($id: ID!) {
  deleteUser(id: $id) {
    success
    message
  }
}
EOF

# View the mutations
echo "=== Create Mutation ==="
cat create-user-mutation.graphql
echo ""
echo "=== Update Mutation ==="
cat update-user-mutation.graphql
echo ""
echo "=== Delete Mutation ==="
cat delete-user-mutation.graphql
```

**Tasks**:
1. Write a mutation for creating a blog post
2. Write a mutation for adding a comment
3. Write a mutation for liking a post
4. Include proper error handling in the response

---

## Exercise 7: Complex Query Building

**Goal**: Combine everything learned into complex queries.

### Create a Comprehensive Query Script
```bash
cat > complex-country-query.sh << 'EOF'
#!/bin/bash

echo "=== Complex Country Analysis ==="
echo ""

# 1. Get continent statistics
echo "1. Continent Statistics:"
gql https://countries.trevorblades.com/ \
  -q '{
    africa: countries(filter: { continent: { eq: "AF" } }) { code }
    europe: countries(filter: { continent: { eq: "EU" } }) { code }
    asia: countries(filter: { continent: { eq: "AS" } }) { code }
  }' | jq '{
    africa_count: (.data.africa | length),
    europe_count: (.data.europe | length),
    asia_count: (.data.asia | length)
  }'

echo ""

# 2. Get detailed country comparison
echo "2. Country Comparison:"
gql https://countries.trevorblades.com/ \
  -q '{
    developing: country(code: "KE") {
      name
      currency
      languages { name }
    }
    developed: country(code: "US") {
      name
      currency
      languages { name }
    }
  }' | jq '.data'

echo ""
echo "Done!"
EOF

chmod +x complex-country-query.sh
./complex-country-query.sh
```

### SpaceX Analysis Script
```bash
cat > spacex-analysis.sh << 'EOF'
#!/bin/bash

echo "=== SpaceX Launch Analysis ==="

# Get launch statistics
gql https://api.spacex.land/graphql/ \
  -q '{
    launchesPast(limit: 20) {
      mission_name
      launch_year
      launch_success
    }
  }' | jq '
    .data.launchesPast |
    group_by(.launch_year) |
    map({
      year: .[0].launch_year,
      total: length,
      successful: map(select(.launch_success == true)) | length
    })
  '
EOF

chmod +x spacex-analysis.sh
./spacex-analysis.sh
```

**Tasks**:
1. Create a script that analyzes countries by continent
2. Build a query that gets SpaceX launch success rates
3. Create a comparative analysis of multiple countries

---

## Exercise 8: Error Handling and Debugging

**Goal**: Learn to handle and debug GraphQL errors.

### Intentional Errors for Learning
```bash
# Invalid field name
gql https://countries.trevorblades.com/ \
  -q 'query { countries { invalidField } }' 2>&1 | jq '.'

# Missing required argument
gql https://countries.trevorblades.com/ \
  -q 'query { country { name } }' 2>&1 | jq '.'

# Wrong variable type
cat > error-test.graphql << 'EOF'
query GetCountry($code: Int!) {
  country(code: $code) {
    name
  }
}
EOF

echo '{"code": 123}' > error-vars.json
gql https://countries.trevorblades.com/ \
  --queryFile error-test.graphql \
  --variablesFile error-vars.json 2>&1 | jq '.'
```

### Create Error Handler Script
```bash
cat > graphql-safe-query.sh << 'EOF'
#!/bin/bash

API=$1
QUERY=$2

if [ -z "$API" ] || [ -z "$QUERY" ]; then
    echo "Usage: $0 <api-url> <query>"
    exit 1
fi

RESPONSE=$(gql "$API" -q "$QUERY" 2>&1)
ERRORS=$(echo "$RESPONSE" | jq -r '.errors // empty')

if [ -n "$ERRORS" ]; then
    echo "❌ Error occurred:"
    echo "$RESPONSE" | jq '.errors'
    exit 1
else
    echo "✅ Success:"
    echo "$RESPONSE" | jq '.data'
fi
EOF

chmod +x graphql-safe-query.sh

# Test it
./graphql-safe-query.sh \
  https://countries.trevorblades.com/ \
  '{ countries { code name } }'
```

**Tasks**:
1. Test various error scenarios
2. Create a script that validates queries before executing
3. Build error logging into your query scripts

---

## Exercise 9: Performance Optimization

**Goal**: Learn to optimize GraphQL queries.

### Measure Query Performance
```bash
# Benchmark different query sizes
cat > benchmark-queries.sh << 'EOF'
#!/bin/bash

echo "=== Query Performance Comparison ==="

# Small query
echo "Small query (2 fields):"
time gql https://countries.trevorblades.com/ \
  -q '{ countries { code name } }' > /dev/null

echo ""

# Medium query
echo "Medium query (5 fields):"
time gql https://countries.trevorblades.com/ \
  -q '{ countries { code name capital currency phone } }' > /dev/null

echo ""

# Large query with nesting
echo "Large nested query:"
time gql https://countries.trevorblades.com/ \
  -q '{ 
    countries { 
      code 
      name 
      capital 
      currency 
      languages { code name }
      continent { code name }
    } 
  }' > /dev/null
EOF

chmod +x benchmark-queries.sh
./benchmark-queries.sh
```

### Compare Response Sizes
```bash
# Compare data payload sizes
echo "=== Response Size Comparison ==="

echo "Minimal query:"
gql https://countries.trevorblades.com/ \
  -q '{ countries { code } }' | wc -c

echo "Full query:"
gql https://countries.trevorblades.com/ \
  -q '{ countries { code name capital currency phone } }' | wc -c
```

**Tasks**:
1. Compare query times for different nesting levels
2. Measure bandwidth savings vs REST
3. Find the optimal field selection for your use case

---

## Exercise 10: Build a GraphQL CLI Tool

**Goal**: Create a reusable tool for GraphQL exploration.

```bash
cat > graphql-explorer.sh << 'EOF'
#!/bin/bash

# GraphQL Explorer Tool
# Usage: ./graphql-explorer.sh <command> [args]

COUNTRIES_API="https://countries.trevorblades.com/"
SPACEX_API="https://api.spacex.land/graphql/"

show_help() {
    echo "GraphQL Explorer - A CLI tool for exploring GraphQL APIs"
    echo ""
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  schema <api>           - Show schema for API (countries|spacex)"
    echo "  country <code>         - Get country details"
    echo "  continent <code>       - Get continent details"
    echo "  launches <limit>       - Get SpaceX launches"
    echo "  compare <code1> <code2> - Compare two countries"
    echo ""
}

get_schema() {
    case $1 in
        countries)
            gql $COUNTRIES_API --introspect | jq '.data.__schema.types[] | select(.kind == "OBJECT") | .name'
            ;;
        spacex)
            gql $SPACEX_API --introspect | jq '.data.__schema.types[] | select(.kind == "OBJECT") | .name'
            ;;
        *)
            echo "Unknown API. Use: countries or spacex"
            ;;
    esac
}

get_country() {
    gql $COUNTRIES_API -q "
      query {
        country(code: \"$1\") {
          code
          name
          capital
          currency
          continent { name }
          languages { name }
        }
      }
    " | jq '.data.country'
}

get_continent() {
    gql $COUNTRIES_API -q "
      query {
        continent(code: \"$1\") {
          code
          name
          countries {
            code
            name
          }
        }
      }
    " | jq '.data.continent'
}

get_launches() {
    gql $SPACEX_API -q "
      query {
        launchesPast(limit: $1) {
          mission_name
          launch_date_local
          rocket {
            rocket_name
          }
        }
      }
    " | jq '.data.launchesPast'
}

compare_countries() {
    gql $COUNTRIES_API -q "
      query {
        first: country(code: \"$1\") {
          name
          capital
          currency
          languages { name }
        }
        second: country(code: \"$2\") {
          name
          capital
          currency
          languages { name }
        }
      }
    " | jq '.data'
}

# Main command router
case $1 in
    schema)
        get_schema $2
        ;;
    country)
        get_country $2
        ;;
    continent)
        get_continent $2
        ;;
    launches)
        get_launches ${2:-5}
        ;;
    compare)
        compare_countries $2 $3
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

chmod +x graphql-explorer.sh

# Test the tool
echo "Testing GraphQL Explorer:"
./graphql-explorer.sh help
```

**Tasks**:
1. Add more commands to the tool
2. Add error handling
3. Add output formatting options (table, json, csv)
4. Add support for custom queries

---

## Challenge Exercises

Ready for advanced challenges?

1. **Build a GraphQL Cache**: Create a script that caches query responses

2. **Query Optimizer**: Analyze queries and suggest optimizations

3. **API Comparator**: Compare multiple GraphQL APIs side-by-side

4. **Data Exporter**: Export GraphQL data to different formats

5. **Query Builder**: Interactive script to build queries step-by-step

---

## Verification Checklist

After completing Phase 2 exercises, you should be able to:

- [ ] Write nested queries with multiple levels
- [ ] Use arguments to filter and sort data
- [ ] Use aliases to query the same field multiple times
- [ ] Create and use fragments effectively
- [ ] Write queries with variables
- [ ] Understand mutation syntax and structure
- [ ] Handle GraphQL errors gracefully
- [ ] Optimize queries for performance
- [ ] Build shell scripts for GraphQL operations
- [ ] Compare GraphQL to REST in practice

---

## Next Steps

Congratulations! You've mastered consuming GraphQL APIs. In Phase 3, you'll:
1. Build your own GraphQL server
2. Define custom schemas
3. Implement resolvers
4. Handle real data

**Tip**: Keep these exercises handy - they're useful for testing your own APIs!
