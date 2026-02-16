import { Hono } from 'hono'
import { Database } from "bun:sqlite";

const app = new Hono()

const db = new Database("database.sqlite");

db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE
  )
`)

// Get All Users
app.get("/users", (c) => {
  const users = db.prepare("SELECT * FROM users").all();
  return c.json(users);
})

// Get User by Email
app.get("/users/:email", (c) => {
  const { email } = c.req.param();
  const user = db.prepare("SELECT * FROM users WHERE email = ?").get(email);

  if (!user) {
    return c.json({ message: "User not found" }, 404);
  }

  return c.json(user);
})

// Create User
app.post("/users", async (c) => {
  const { name, email } = await c.req.json();

  try {
    const stmt = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
    const result = stmt.run(name, email);

    return c.json({
      id: result.lastInsertRowid,
      name,
      email
    }, 201);
  } catch (error) {
    return c.json({
      message: "Error creating user. Email might already exist.",
      error: error instanceof Error ? error.message : String(error)
    }, 400);
  }
})

// Delete User by Email
app.delete("/users/:email", (c) => {
  const { email } = c.req.param();

  const result = db.prepare("DELETE FROM users WHERE email = ?").run(email);

  if (result.changes === 0) {
    return c.json({ message: "No user found with this email" }, 404);
  }

  return c.json({
    message: "User deleted successfully",
    deletedCount: result.changes
  });
})

// Update Name by Email
app.patch("/users/name", async (c) => {
  const { email, newName } = await c.req.json();

  const result = db.prepare("UPDATE users SET name = ? WHERE email = ?").run(newName, email);

  if (result.changes === 0) {
    return c.json({ message: "No user found with this email" }, 404);
  }

  return c.json({
    message: "Name updated successfully",
    updatedCount: result.changes
  });
})

// Update Email
app.patch("/users/email", async (c) => {
  const { currentEmail, newEmail } = await c.req.json();

  try {
    const result = db.prepare("UPDATE users SET email = ? WHERE email = ?").run(newEmail, currentEmail);

    if (result.changes === 0) {
      return c.json({ message: "No user found with this email" }, 404);
    }

    return c.json({
      message: "Email updated successfully",
      updatedCount: result.changes
    });
  } catch (error) {
    return c.json({
      message: "Error updating email. New email might already exist.",
      error: error instanceof Error ? error.message : String(error)
    }, 400);
  }
})

// Delete All Users
app.delete("/users", (c) => {
  const result = db.prepare("DELETE FROM users").run();

  return c.json({
    message: "All users deleted successfully",
    deletedCount: result.changes
  });
})

// Custom SQL execution
app.post("/execute-query", async (c) => {
  try {
    const { query, params } = await c.req.json();

    if (!query || typeof query !== 'string') {
      return c.json({
        error: "Invalid query. A valid SQL query string is required."
      }, 400);
    }

    const allowedQueryTypes = ['SELECT', 'INSERT', 'UPDATE', 'DELETE'];
    const queryType = query.trim().split(/\s+/)[0].toUpperCase();

    if (!allowedQueryTypes.includes(queryType)) {
      return c.json({
        error: "Unauthorized query type. Only SELECT, INSERT, UPDATE, and DELETE are allowed."
      }, 403);
    }

    const forbiddenPatterns = [
      /DROP\s+TABLE/i,
      /TRUNCATE/i,
      /ALTER\s+TABLE/i,
      /CREATE\s+TABLE/i,
      /PRAGMA/i,
      /;/  // Prevent multiple statements
    ];

    const hasForbiddenPattern = forbiddenPatterns.some(pattern => pattern.test(query));
    if (hasForbiddenPattern) {
      return c.json({
        error: "Query contains potentially dangerous operations"
      }, 403);
    }

    if (!Array.isArray(params)) {
      return c.json({
        error: "Parameters must be an array"
      }, 400);
    }

    const stmt = db.prepare(query);

    let result;
    switch (queryType) {
      case 'SELECT':
        result = stmt.all(...params);
        return c.json({
          success: true,
          data: result
        });

      case 'INSERT':
        result = stmt.run(...params);
        return c.json({
          success: true,
          lastInsertRowid: result.lastInsertRowid,
          changes: result.changes
        });

      case 'UPDATE':
      case 'DELETE':
        result = stmt.run(...params);
        return c.json({
          success: true,
          changes: result.changes
        });

      default:
        return c.json({
          error: "Unsupported query type"
        }, 400);
    }

  } catch (error) {
    console.error("Query execution error:", error);

    return c.json({
      error: "Failed to execute query",
      details: error instanceof Error ? error.message : String(error)
    }, 500);
  }
});

// Root route
app.get('/', (c) => {
  return c.text("Hello, World!")
})

export default {
  fetch: app.fetch,
  port: 3000,
  hostname: '0.0.0.0'
}
