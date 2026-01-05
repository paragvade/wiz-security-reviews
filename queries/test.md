# Wiz GraphQL Queries

This directory contains GraphQL queries for interacting with the Wiz API. These queries are used for security reviews, role auditing, and cloud account management.

## Available Queries

### 1. [Get Role Permissions](./get_role_permissions.graphql)
Retrieves detailed permissions (scopes) for a specific Wiz role.

**Key Features:**
- Works with both built-in roles (e.g., `PROJECT_READER`) and custom roles (UUID-based)
- Returns all permission scopes for the role
- Includes role description and metadata
- Retrieves detailed permissions (scopes) for a specific Wiz role. Useful for understanding role capabilities, comparing roles, and auditing access levels.
- Wiz uses two different ID formats depending on whether the role is built-in or custom
- Built-in Roles --> Uppercase string constant e.g. PROJECT_READER
- Custom Role --> UUID (36-character hex string) e.g. 6fefaaf7-c4d7-4e38-8049-c367103c8392
- To find the ID for a custom role, first list all roles: