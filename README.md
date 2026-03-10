# postgres_ai

[![PyPI version](https://badge.fury.io/py/postgres_ai.svg)](https://pypi.org/project/postgres_ai/)
[![Python versions](https://img.shields.io/pypi/pyversions/postgres_ai.svg)](https://pypi.org/project/postgres_ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**postgres_ai** is an open-source **MCP (Model Context Protocol) server** for PostgreSQL databases.  
It bridges LLMs (like Claude, GPT, etc.) with your Postgres data by letting you define custom **"skills"** in markdown files.  

Using the **SKILL Graph** technique, it enables dynamic, on-demand context expansion — preventing LLM overload while scaling complexity through interconnected skills.

Built on **FastMCP** + **asyncpg**.

## Features

- Async PostgreSQL integration
- Custom skills defined in markdown (`SKILL.md` with YAML frontmatter)
- Dynamic skill graph loading (`load_skill`, `read_business_logic`, `execute_query`)
- MCP-compliant server (compatible with LLM clients that support Model Context Protocol)
- Environment-based configuration + CLI overrides
- Interactive password prompt for quick testing
- Structured logging

## Installation

```bash
uv add postgres_ai
```
or
```bash
pip install postgres_ai
```

**Build the Skill Files**
- In the CWD, create the skill directory and grow your skill directory according to your business needs and objectives
- Note: Always should have a business_logic sub-directory inside your skill dir.
- For reference checkout out this repository's `pg_skills` directory.

**Prerequisites**
- Python ≥ 3.12
- PostgreSQL server (local or remote)
- Add the respective skills and modify the respective skill file according to your business need/objective

## Quick Start

1. Create a `.env` file (or use CLI flags):

   ```env
   # .env
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASS=your_secure_password
   DB_NAME=your_database

   # Optional MCP server settings
   # MCP_SERVER_HOST=0.0.0.0
   # MCP_SERVER_PORT=8000
   # MCP_SERVER_TRANSPORT=streamable-http
   ```

2. Start the server:

   See full options:
   ```bash
   postgres_ai --help
   ```
   1. Customize where to serve your MCP Server
   ```bash
   postgres_ai --host <your host> --port <your port>
   ```
   2. If configured in the .env, directly run
   ```bash
   postgres_ai
   ```
   3. Or configure them through the cli
   ```bash
   postgres_ai --db-host --db-port --db-user --db-name --prompt-password
   ```

3. Connect an LLM client that supports MCP (e.g., Claude with custom tools) and call the exposed tools:
   - `read_business_logic()`
   - `load_skill(skill_name: str)`
   - `execute_query(sql_query: str)`

Skills live in a `pg_skills/` folder next to your client code (or wherever your MCP client expects them).


## Usage & Skills

Skills are stored as markdown files inside subfolders:

```
pg_skills/
├── business-logic/
│   └── SKILL.md          # default / root logic
└── customer-support/
    └── SKILL.md          # can reference other skills
```

**SKILL.md example structure**:

```markdown
---
name: customer-support
description: Handles customer queries by querying orders and support tickets
depends_on: [business-logic]
---

## Instructions for the model

You are a helpful support agent. Use execute_query only when needed.
...
```

The server dynamically loads and expands context via the skill graph.

Logs are written to `mcp_logs/pg_ai_log.log` (configurable).

## Development / Contributing

Want to add features, fix bugs, or improve docs?

1. Clone & install editable:

   ```bash
   git clone https://github.com/saiprasaad2002/pg_ai.git
   cd pg_ai
   uv venv --python 3.12
   source .venv/bin/activate
   uv pip install -e .
   ```

2. Make changes → test with `postgres_ai --prompt-password`

3. Commit, push, open a PR!

## License

MIT License — see [LICENSE](LICENSE)

## Links

- 📦 [PyPI: postgres_ai](https://pypi.org/project/postgres_ai/)
- 🌐 [GitHub Repository](https://github.com/saiprasaad2002/pg_ai)
- 📧 Issues / questions → open an issue!


Built with ❤️ in Chennai.
