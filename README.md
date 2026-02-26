# pg_ai  <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Logo_PostgreSQL.png" alt="PostgreSQL" width="100">
[![GitHub license](https://img.shields.io/github/license/saiprasaad2002/pg_ai)](https://github.com/saiprasaad2002/pg_ai/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/saiprasaad2002/pg_ai)](https://github.com/saiprasaad2002/pg_ai/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/saiprasaad2002/pg_ai)](https://github.com/saiprasaad2002/pg_ai/issues)

## Overview

pg_ai is an open-source MCP (Model Context Protocol) server tailored for PostgreSQL databases. It bridges LLMs with your Postgres data by allowing users to define custom "skills" — encapsulated business logic in markdown files — that guide intelligent database interactions. By implementing the SKILL Graph technique, pg_ai enables dynamic, on-demand context expansion, preventing LLM overload while scaling complexity through interconnected skills.

Inspired by Anthropic's Claude Skills and the SKILL Graph concept (as discussed in [this X thread](https://x.com/arscontexta/status/2023957499183829467?s=20)), pg_ai turns your database into a contextual powerhouse for AI agents.

## Key Features

- **Postgres Integration**: Asynchronous connections for efficient querying.
- **Skill Management**: Load custom skills from markdown files (SKILL.md) in a progressive, token-efficient manner.
- **Dynamic Context Growth**: Use SKILL Graph to link and load skills on-demand, building a network of reusable logic.
- **MCP Compliance**: Exposes tools for LLMs to read business logic, load specific skills, and execute SQL queries.
- **Logging and Configurability**: Environment-based setup with dedicated logging.

## Architecture

pg_ai is built on FastMCP (a FastAPI-based MCP implementation) and uses asyncpg for PostgreSQL interactions. The core components include:

1. **Server Setup (app.py)**: Initializes the MCP server with a lifespan hook for database connection management.
2. **PgMCP Class (src/mcp_server/server.py)**: Wraps FastMCP to configure the server with tools and lifespan.
3. **Postgres Connector (src/connectors/pg_connector.py)**: Handles async connect/disconnect to Postgres using the `databases` library.
4. **Environment Loader (src/loaders/env_loader.py)**: Loads settings from `.env` using Pydantic for validation.
5. **Logger (src/logger/mcp_logger.py)**: Configures file-based logging for server events.
6. **Tools (src/mcp_tools/tools.py)**: Defines MCP tools:
   - `read_business_logic()`: Loads default business logic from `pg_skills/business-logic/SKILL.md`.
   - `load_skill(skill_name)`: Dynamically loads a specific skill's instructions from `pg_skills/<skill_name>/SKILL.md`.
   - `execute_query(sql_query)`: Executes SQL queries on the connected Postgres DB and returns results as a Polars DataFrame.

The SKILL Graph is realized through interconnected skills: Each SKILL.md can reference other skills, allowing the LLM to traverse the graph by calling `load_skill` as needed. This grows context incrementally, aligning with MCP's goal of efficient external system integration.

## Installation

### Prerequisites
- Python >= 3.12
- PostgreSQL database
- Git

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/saiprasaad2002/pg_ai.git
   cd pg_ai
   ```

2. Install dependencies:
   ```
   uv sync
   ```

3. Copy and configure the environment file:
   ```
   cp .env.example .env
   ```
   Edit `.env` with your Postgres credentials and MCP server settings:
   - `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, `DB_NAME`: Postgres connection details.
   - `MCP_SERVER_HOST`, `MCP_SERVER_PORT`, `MCP_SERVER_TRANSPORT`: Server config (e.g., `STREAMABLE-HTTP` for production).

4. Run the server:
   ```
   uv run app.py
   ```

The server will start, connect to your Postgres DB, and expose MCP endpoints.

## Usage

### Adding Skills
Skills are stored in the `pg_skills/` directory. Each skill is a subfolder containing a `SKILL.md` file.

- **Structure Example**:
  ```
  pg_skills/
  ├── business-logic/
  │   └── SKILL.md  # Default business logic (e.g., table schemas, query guidelines)
  └── custom-skill/
      └── SKILL.md  # Custom skill instructions (YAML frontmatter + Markdown body)
  ```

- **SKILL.md Format** (Inspired by Claude Skills):
  - **YAML Frontmatter**: Minimal metadata (name, description) for progressive disclosure.
  - **Body**: Detailed instructions, examples, or business logic for the LLM.
  - Example:
    ```
    ---
    name: inventory-check
    description: Checks inventory levels in the products table. Use when querying stock.
    ---

    # Inventory Check Skill

    To check inventory:
    1. Query the `products` table: SELECT * FROM products WHERE id = {id};
    2. Analyze stock levels.
    ...
    ```

Skills can reference others (e.g., "Load the 'reporting' skill for summaries"), forming a graph for dynamic loading.

### Interacting with the Server
- Connect your LLM (e.g., Claude, ChatGPT) via an MCP client.
- The LLM can call tools to load skills and execute queries, building context as needed.
- Logs are saved in `mcp_logs/pg_ai_log.log`.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Commit changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Claude Skills Blog](https://www.anthropic.com/news/skills)
- [SKILL Graph Discussion](https://x.com/arscontexta/status/2023957499183829467?s=20)

For questions, open an issue or contact the maintainer.
