import { Hono } from 'hono'
import { Database } from "bun:sqlite";

const app = new Hono()

const db = new Database("database.sqlite");
const query = db.query("select 'Hello world' as message;");
query.get();

app.get('/', (c) => {
  return c.text("Hello, World!")
})

export default {
  fetch: app.fetch,
  port: 3000,
  hostname: '0.0.0.0'
}