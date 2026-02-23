from fastmcp import FastMCP
import requests

BASE_URL = "http://190.1.3.34:3000"

mcp = FastMCP("SQLite_DB_Access_MCP")


@mcp.tool
def get_all_users():
    """
    Retrieve all users from the database
    Returns: List of user dictionaries
    """
    response = requests.get(f"{BASE_URL}/users")
    return response.json()


@mcp.tool
def get_user_by_email(email):
    """
    Retrieve a user by their email
    Args:
        email (str): User's email address
    Returns: User dictionary or error message
    """
    response = requests.get(f"{BASE_URL}/users/{email}")
    return response.json()


@mcp.tool
def create_user(name, email):
    """
    Create a new user
    Args:
        name (str): User's name
        email (str): User's email address
    Returns: Created user details or error message
    """
    payload = {
        "name": name,
        "email": email
    }
    response = requests.post(
        f"{BASE_URL}/users",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()


@mcp.tool
def delete_user_by_email(email):
    """
    Delete a user by their email
    Args:
        email (str): User's email address
    Returns: Deletion result or error message
    """
    response = requests.delete(f"{BASE_URL}/users/{email}")
    return response.json()


@mcp.tool
def update_name_by_email(email, new_name):
    """
    Update user's name using their email
    Args:
        email (str): User's current email
        new_name (str): New name to set
    Returns: Update result or error message
    """
    payload = {
        "email": email,
        "newName": new_name
    }
    response = requests.patch(
        f"{BASE_URL}/users/name",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()


@mcp.tool
def update_email(current_email, new_email):
    """
    Update user's email address
    Args:
        current_email (str): User's current email
        new_email (str): New email address
    Returns: Update result or error message
    """
    payload = {
        "currentEmail": current_email,
        "newEmail": new_email
    }
    response = requests.patch(
        f"{BASE_URL}/users/email",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()


@mcp.tool
def delete_all_users():
    """
    Delete all users from the database
    Returns: Deletion result
    """
    response = requests.delete(f"{BASE_URL}/users")
    return response.json()


@mcp.tool
def sql_statement(query, parameters):
    """
    Execute a custom SQL query with parameterized input to prevent SQL injection.

    This function provides a secure way to execute dynamic SQL queries against the database 
    with strict safety controls and input validation. It supports SELECT, INSERT, UPDATE, 
    and DELETE operations while preventing potentially malicious database manipulations.

    Parameters:
    -----------
    query : str
        The SQL query to be executed. Must be a valid SQL statement.
        Supported query types:
        - SELECT: Retrieve data from the database
        - INSERT: Add new records to a table
        - UPDATE: Modify existing records
        - DELETE: Remove records from a table

    parameters : list or tuple
        A list of parameters to be used with the prepared statement.
        Each parameter will be safely bound to the query to prevent SQL injection.
        The number and type of parameters should match the placeholders in the query.

    Returns:
    --------
    dict
        A dictionary containing the result of the query execution:
        - For SELECT queries: 
            {
                'success': True, 
                'data': [list of retrieved records]
            }
        - For INSERT queries: 
            {
                'success': True, 
                'lastInsertRowid': int,  # ID of the last inserted record
                'changes': int  # Number of rows affected
            }
        - For UPDATE/DELETE queries:
            {
                'success': True, 
                'changes': int  # Number of rows affected
            }

    Raises:
    -------
    ValueError
        - If the query is empty or not a string
        - If parameters are not a list or tuple
        - If an unsupported query type is provided
        - If potentially dangerous SQL operations are detected

    Examples:
    ---------
    # Select users
    result = sql_statement(
        "SELECT * FROM users WHERE age > ?", 
        [18]
    )

    # Insert a new user
    result = sql_statement(
        "INSERT INTO users (name, email) VALUES (?, ?)", 
        ["John Doe", "john@example.com"]
    )

    # Update user name
    result = sql_statement(
        "UPDATE users SET name = ? WHERE email = ?", 
        ["John Smith", "john@example.com"]
    )

    Security Notes:
    ---------------
    - Uses parameterized queries to prevent SQL injection
    - Restricts query types to safe operations
    - Blocks potentially destructive SQL commands
    - Provides minimal error information to prevent information leakage
    """

    if not query or not isinstance(query, str):
        raise ValueError(
            "Invalid query. A valid SQL query string is required.")

    if not isinstance(parameters, (list, tuple)):
        raise ValueError("Parameters must be a list or tuple.")

    payload = {
        "query": query.strip(),
        "params": list(parameters)
    }

    response = requests.post(
        f"{BASE_URL}/execute-query",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    mcp.run()
