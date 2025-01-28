# AuraConnection: Neo4j Aura Python Utility

## Overview

The `AuraConnection` class provides a Python utility for managing connections and executing Cypher queries on a **Neo4j Aura** instance. It simplifies tasks such as establishing a connection, testing connectivity, and running Cypher queries.

This utility is designed to ensure secure, reliable, and efficient interaction with a Neo4j Aura database using the official Neo4j Python driver.

---

## Features

- **Environment Variable Configuration**: Securely loads connection credentials from a `.env` file.
- **Logging**: Integrated logging for monitoring connection status and errors.
- **Connection Pooling**: Optimized settings for Neo4j Aura instances.
- **Query Execution**: Easily run Cypher queries and retrieve results.
- **Error Handling**: Comprehensive error logging for troubleshooting.

---

## Prerequisites

- Python 3.8 or later
- A **Neo4j Aura** database instance
- The following Python libraries:
  - `neo4j`
  - `python-dotenv`

Install dependencies using:
```bash
pip install neo4j python-dotenv
```

---

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a `.env` File**:
   Add your Neo4j Aura credentials in a `.env` file at the root of the project:
   ```ini
   NEO4J_URI=neo4j+s://<your-database-uri>
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=<your-password>
   ```

3. **Run the Script**:
   Execute the main script to connect to your database and test the connection:
   ```bash
   python <script_name>.py
   ```

---

## Code Usage

### **Class: `AuraConnection`**

#### **Initialization**
```python
aura = AuraConnection()
```

#### **Methods**
1. **`connect()`**: Establishes a connection to the Neo4j Aura database.
   ```python
   success = aura.connect()
   ```

2. **`close()`**: Closes the connection.
   ```python
   aura.close()
   ```

3. **`test_connection()`**: Tests the connection with a basic query.
   ```python
   is_connected = aura.test_connection()
   ```

4. **`execute_query(query: str, parameters: dict = None)`**: Executes a Cypher query and returns the results.
   ```python
   query = "MATCH (n) RETURN count(n) as node_count"
   result = aura.execute_query(query)
   print(result)
   ```

---

## Example Workflow

1. Initialize the `AuraConnection` class.
2. Connect to the database using `connect()`.
3. Verify the connection with `test_connection()`.
4. Execute queries with `execute_query(query, parameters)`.
5. Close the connection with `close()`.

Example:
```python
aura = AuraConnection()

try:
    if aura.connect():
        if aura.test_connection():
            print("Connected to Neo4j Aura!")
            result = aura.execute_query("MATCH (n) RETURN count(n) AS count")
            print(f"Node count: {result[0]['count']}")
finally:
    aura.close()
```

---

## Environment Variables

| Variable         | Description                       | Example                                     |
|-------------------|-----------------------------------|---------------------------------------------|
| `NEO4J_URI`       | Neo4j Aura connection URI        | `neo4j+s://<instance-id>.databases.neo4j.io` |
| `NEO4J_USERNAME`  | Username for authentication      | `neo4j`                                    |
| `NEO4J_PASSWORD`  | Password for authentication      | `<your-password>`                          |

---

## Logging

Logs are written to the console for monitoring connection status and errors. You can customize logging behavior by modifying the `logging.basicConfig()` settings.

---

## Notes

- Ensure the `.env` file is included in `.gitignore` to prevent sensitive information from being exposed.
- The script requires an active Neo4j Aura instance with valid credentials.

---

## License

This project is licensed under the MIT License.

---

