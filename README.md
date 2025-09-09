# LLM Knowledge Extractor

A FastAPI-based service that extracts structured knowledge from text using LLM analysis and custom keyword extraction.

## Setup and Run

### Prerequisites

- Python 3.11+
- Docker

### Quick Start

- Copy and paste the env.example and save it as .env
- Update the `<OPENAI_API_KEY>` ENV Var with your key.

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up --build
```

### MakeFile

Run the command

```bash
make help
```

and use the displayed commands the for project

### Testing

After you have started the project run:

```bash
# Run tests
docker-compose exec app pytest
```

### API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Design Choices

I structured this codebase with a clean, layered architecture separating concerns: **FastAPI** for the web layer with automatic OpenAPI documentation, **SQLAlchemy** with async support for robust database operations, and **Alembic** for database migrations. The service layer acts as a business logic coordinator, while the database layer includes generic helpers like `get_one_or_error()` to eliminate repetitive error handling patterns. I chose **Pydantic** for data validation and serialization, and **PostgreSQL** for its JSON support and reliability. The modular structure with separate directories for API endpoints, services, database models, and utilities makes the codebase maintainable and testable.

## Trade-offs

Due to time constraints, I focused on core functionality over extensive testing. I would have liked to add database transaction tests. Additionally, I would have implemented more robust error handling for edge cases and added performance monitoring/metrics collection.
