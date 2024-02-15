1. **What’s a database?**
   - A database is an organized collection of structured data, typically stored and accessed electronically from a computer system. It allows users to easily manage, manipulate, and retrieve data as needed.

2. **What’s a relational database?**
   - A relational database is a type of database that organizes data into one or more tables where data can be related to each other through common attributes. It relies on a relational model based on mathematical set theory and represents data in the form of rows and columns.

3. **What does SQL stand for?**
   - SQL stands for Structured Query Language. It is a standard programming language used for managing relational databases. SQL is used to perform various operations such as querying data, updating data, defining and modifying schema, and managing permissions.

4. **What’s MySQL?**
   - MySQL is an open-source relational database management system (RDBMS) based on SQL. It is one of the most popular databases in the world and is widely used for web applications, especially in conjunction with the LAMP (Linux, Apache, MySQL, PHP/Python/Perl) stack.

5. **How to create a database in MySQL?**
   - To create a database in MySQL, you can use the `CREATE DATABASE` statement followed by the name of the database you want to create. For example:
     ```sql
     CREATE DATABASE dbname;
     ```

6. **What does DDL and DML stand for?**
   - DDL stands for Data Definition Language, which is used to define and manage the structure of database objects such as tables, indexes, and constraints. Examples of DDL statements include `CREATE`, `ALTER`, `DROP`, etc.
   - DML stands for Data Manipulation Language, which is used to manipulate data stored in the database. Examples of DML statements include `SELECT`, `INSERT`, `UPDATE`, `DELETE`, etc.

7. **How to CREATE or ALTER a table?**
   - To create a table in MySQL, you can use the `CREATE TABLE` statement followed by the table name and the columns and their data types. For example:
     ```sql
     CREATE TABLE tablename (
         column1 datatype,
         column2 datatype,
         ...
     );
     ```
   - To alter an existing table in MySQL, you can use the `ALTER TABLE` statement followed by the table name and the alteration you want to make. For example:
     ```sql
     ALTER TABLE tablename ADD COLUMN column3 datatype;
     ```

8. **How to SELECT data from a table?**
   - To select data from a table in MySQL, you can use the `SELECT` statement followed by the columns you want to retrieve and the table you want to retrieve them from. For example:
     ```sql
     SELECT column1, column2 FROM tablename;
     ```

9. **How to INSERT, UPDATE or DELETE data?**
   - To insert data into a table, you can use the `INSERT INTO` statement followed by the table name and the values you want to insert. For example:
     ```sql
     INSERT INTO tablename (column1, column2) VALUES (value1, value2);
     ```
   - To update existing data in a table, you can use the `UPDATE` statement followed by the table name, the columns you want to update, and the new values. For example:
     ```sql
     UPDATE tablename SET column1 = value1 WHERE condition;
     ```
   - To delete data from a table, you can use the `DELETE FROM` statement followed by the table name and a condition that specifies which rows to delete. For example:
     ```sql
     DELETE FROM tablename WHERE condition;
     ```

10. **What are subqueries?**
    - Subqueries, also known as nested queries or inner queries, are queries nested within another SQL query. They are used to retrieve data based on the result of another query. Subqueries can be used in SELECT, INSERT, UPDATE, and DELETE statements.

11. **How to use MySQL functions?**
    - MySQL provides a wide range of built-in functions for performing various operations on data. These functions can be used in SQL queries to manipulate data, perform calculations, format output, and more. Examples of MySQL functions include `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`, `CONCAT`, `SUBSTRING`, `DATE_FORMAT`, etc.
