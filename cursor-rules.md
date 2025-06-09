# CVGenius Project Cursor Rules

## Project Overview
This is a serverless web application for CV/Resume generation and optimization using AI. Built with FastAPI (Python) backend and Next.js (TypeScript) frontend.

## Code Style & Standards

### Python (Backend)
- Use Python 3.11+ type hints everywhere
- Follow PEP 8 style guide
- Use Black for formatting
- Use FastAPI with Pydantic models for validation
- Prefer async/await for I/O operations
- Use descriptive variable and function names
- Add docstrings to all functions and classes

### TypeScript/React (Frontend)
- Use TypeScript strict mode
- Prefer functional components with hooks
- Use Tailwind CSS for styling
- Follow React best practices (proper key props, avoid inline functions in render)
- Use proper TypeScript interfaces for all data structures
- Prefer const assertions and as const
- Use descriptive component and variable names

### File Naming Conventions
- Backend: snake_case for Python files
- Frontend: PascalCase for React components, camelCase for utilities
- Use descriptive names that indicate purpose

## Architecture Principles
- Stateless design - no user data persistence
- Privacy-first approach
- Clean separation between frontend and backend
- Comprehensive error handling
- Input validation at all layers
- Rate limiting for API endpoints

## Dependencies
- Keep dependencies minimal and well-maintained
- Always pin versions in requirements.txt and package.json
- Prefer well-established libraries over experimental ones
- Document any new dependencies and their purpose

## Security
- Never commit API keys or secrets
- Use environment variables for all configuration
- Validate all inputs rigorously
- Implement proper CORS policies
- Use HTTPS everywhere
- Rate limit all endpoints

## Testing
- Write unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Mock external services in tests
- Aim for high test coverage

## Documentation
- Use clear, concise comments where needed
- Document all API endpoints with FastAPI auto-docs
- Keep README updated with setup instructions
- Document environment variables and configuration

## Error Handling
- Use proper HTTP status codes
- Provide meaningful error messages
- Log errors appropriately
- Graceful degradation where possible
- User-friendly error displays in frontend

## Performance
- Optimize bundle sizes
- Use proper caching strategies
- Minimize API calls
- Optimize images and assets
- Monitor and measure performance

When writing code:
1. Focus on readability and maintainability
2. Follow the DRY principle
3. Use meaningful names for variables and functions
4. Handle edge cases and errors
5. Write tests for new functionality
6. Consider security implications
7. Document complex logic
8. Work on Specific folder if doesnt exit, ask to user get his permission 