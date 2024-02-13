

# SQL Basics

## What’s a Database?

A **database** is an organized collection of structured information or data, typically stored electronically in a computer system. It serves as a central repository for storing, managing, and retrieving data. Databases are essential for various applications, from web searches to transaction processing. They can be as simple as a list of contacts or as complex as a global e-commerce platform. The most common types of databases use tables to organize data efficiently.

## Relational Databases

A **relational database** follows the relational model, where data is represented in tables (rows and columns). Each row in a table corresponds to a record, and a unique identifier (usually called a key) distinguishes each record. Relational databases allow efficient querying and manipulation of data.

## SQL (Structured Query Language)

-   **SQL** stands for **Structured Query Language**.
-   It’s an international standard programming language used to manage data in relational database management systems (RDBMS).
-   SQL allows you to query, manipulate, and define data, as well as control access to it. It’s the go-to language for interacting with databases.

## MySQL

-   **MySQL** is the world’s most popular open-source database.
-   It powers many widely used applications, including Facebook, Twitter, Netflix, and more.
-   MySQL offers high performance, reliability, scalability, security, and flexibility.
-   It’s pronounced either “My ess-cue-el” or “my sequel” and has been developed over 25 years in close cooperation with users.

## Common SQL Operations

### Creating a Database in MySQL

To create a new database in MySQL, use the following SQL statement:

```sql
CREATE DATABASE your_database_name;

```

### DDL and DML

-   **DDL (Data Definition Language)**: Used to define and manage the structure of the database (e.g., creating or altering tables).
-   **DML (Data Manipulation Language)**: Used to manipulate data within the database (e.g., inserting, updating, or deleting records).

### SELECT Data from a Table

Use the `SELECT` statement to retrieve specific data from one or more tables:

```sql
SELECT column1, column2 FROM your_table_name WHERE condition;

```

### INSERT, UPDATE, or DELETE Data

-   `INSERT INTO`: Add new records.
-   `UPDATE`: Modify existing records.
-   `DELETE FROM`: Remove records.

## Subqueries

-   **Subqueries** (also known as nested queries) are queries embedded within other queries.
-   They allow you to retrieve data based on conditions from another query’s result.

## Using MySQL Functions

-   MySQL provides various built-in functions for tasks like mathematical calculations, string manipulation, date handling, and more.
-   Use them in your SQL queries to transform or analyze data.

----------
