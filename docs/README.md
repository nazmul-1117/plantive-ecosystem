# 📚 Plantive Ecosystem Documentation

Welcome to the **Plantive** documentation.

This directory contains the technical documentation for the Plantive project, including system architecture, API references, database design, development guides, diagrams, and AI development resources.

The documentation is intended for developers, contributors, and maintainers to better understand, develop, and maintain the project.

---

# 🚀 Quick Links

- [System Architecture](architecture/system-architecture.md)
- [Service Communication](architecture/service-communication.md)
- [API Overview](api/api-overview.md)
- [Database Design](database/database-design.md)
- [Development Setup](development/setup-guide.md)
- [Coding Standards](development/coding-standards.md)
- [Git Workflow](development/git-workflow.md)

---

# 📂 Documentation Structure

```text
docs/
│
├── architecture/
│   ├── system-architecture.md
│   └── service-communication.md
│
├── diagrams/
│   ├── architecture-diagram.png
│   ├── er-diagram.png
│   ├── dfd-level-0.png
│   └── dfd-level-1.png
│
├── api/
│   ├── api-overview.md
│   ├── authentication-api.md
│   ├── plant-api.md
│   ├── garden-api.md
│   └── ai-api.md
│
├── database/
│   ├── database-design.md
│   └── table-descriptions.md
│
├── development/
│   ├── setup-guide.md
│   ├── coding-standards.md
│   └── git-workflow.md
│
└── README.md
```

---

# 📖 Documentation Overview

| Directory | Description |
|-----------|-------------|
| **architecture/** | System architecture, design decisions, and service communication. |
| **diagrams/** | Architecture, ER, DFD, and other system diagrams. |
| **api/** | Backend API documentation, request/response formats, and examples. |
| **database/** | Database schema, relationships, and design documentation. |
| **development/** | Project setup, coding standards, and development workflow. |

---

# 🏗 System Overview

Plantive is built around a layered backend architecture that separates responsibilities across multiple layers to improve maintainability, scalability, and testability.

The primary system components include:

- Android Mobile Application
- FastAPI Backend API
- PostgreSQL Database
- AI Gardening Assistant
- Web API Testing Interface

These components communicate through well-defined APIs and documented workflows.

---

# 📊 Diagrams

The **diagrams/** directory contains visual representations of the system, including:

- System Architecture Diagram
- Entity Relationship (ER) Diagram
- Data Flow Diagrams (DFD)
- Service Interaction Diagrams

Diagrams should be updated whenever significant architectural or database changes are introduced.

---

# 🔌 API Documentation

The **api/** directory documents every backend endpoint.

Each API document should include:

- Endpoint URL
- HTTP Method
- Purpose
- Request Parameters
- Request Body
- Response Schema
- Error Responses
- Authentication Requirements
- Example Requests and Responses

---

# 🗄 Database Documentation

The **database/** directory documents the PostgreSQL database structure.

Documentation should include:

- Table descriptions
- Relationships
- Primary and foreign keys
- Constraints
- Indexes
- Design decisions
- Migration notes (when applicable)

---

# 🛠 Development Guides

The **development/** directory provides guidance for contributors working on the project.

Topics include:

- Local development setup
- Project structure
- Coding standards
- Git workflow
- Best practices

---

# 🤖 AI Development Resources

The **master-prompts/** directory contains reusable prompts used during AI-assisted development.

These prompts help maintain consistency across:

- Backend development
- Database design
- AI service development
- Web API testing

---

# 📖 Documentation Principles

Documentation should always be:

- Accurate
- Up-to-date
- Easy to understand
- Version controlled
- Written in Markdown
- Updated alongside code changes

---

# ✏️ Keeping Documentation Updated

Whenever a feature is added, modified, or removed, update the relevant documentation.

Examples include:

- Add new API endpoints to the API documentation.
- Update database documentation after schema changes.
- Update architecture diagrams when the system design changes.
- Record important design decisions.
- Update setup instructions if dependencies or workflows change.

Keeping documentation synchronized with the codebase helps ensure the project remains maintainable and easy to understand.

---

# 🤝 Contributing

All contributors are encouraged to improve the documentation alongside code changes.

Well-maintained documentation makes onboarding easier, improves collaboration, and helps ensure the long-term maintainability of the Plantive project.

---

🌱 *Plantive Ecosystem aims to create a smart and scalable platform for intelligent plant care.*

---