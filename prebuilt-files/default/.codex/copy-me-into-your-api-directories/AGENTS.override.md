<!-- Move this file into the directory whose files should receive this guidance. -->
<!-- Source template: templates/steering/api.instructions.md -->

# API Design Guidelines

- Use HTTP methods appropriately (GET, POST, PUT, DELETE, PATCH)
- Follow resource-based URL patterns: /api/v1/resources/{id}
- Use plural nouns for resource collections
- Implement proper HTTP status codes
- Include API versioning in URL path
- Use JSON for request and response bodies
- Include pagination for list endpoints
- Implement proper error response format with code, message, and details
- Use JWT tokens for stateless authentication
- Rate limit API endpoints to prevent abuse
