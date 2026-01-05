# Wiz GraphQL Query Reference
This repository contains reusable GraphQL queries for interacting with the Wiz API, enabling automation of common security operations and data retrieval.
This document serves as an index of all available queries, with usage notes and direct links to each file.


---

## Index of Queries

1. [Get All Roles](#get-all-roles) 
2. [Get Role Permissions](#get-role-permissions) 
3. [Get Issues by Account](#get-issues-by-account) - Retrieve security issues for a cloud account

---


## Available Queries

### Get Role Permissions
**Query File:** [`get_role_permissions.graphql`](./get_role_permissions.graphql)
Retrieves detailed permissions (scopes) for a specific Wiz role. Useful for understanding role capabilities, comparing roles, and auditing access levels.

**Key Features:**
- Wiz uses two different ID formats depending on whether the role is built-in or custom
- Built-in Roles --> Uppercase string constant e.g. PROJECT_READER
- Custom Role --> UUID (36-character hex string) e.g. 6fefaaf7-c4d7-4e38-8049-c367103c8392
- To find the ID for a custom role, first [list all roles](./get_all_roles.graphql) and locate your role by name and use its id field.

**Variables:**
```json
{
  "roleId": "PROJECT_READER"
}
```

### Get All Roles
**Query File:** [`get_all_roles.graphql`](./get_all_roles.graphql)
Retrieves a list of all available Wiz roles (both built-in and custom) in your organization. Useful for discovering role IDs needed for the Get Role Permissions query.

**Key Features:**
- Returns all roles with their IDs, names, and descriptions
- Shows both built-in roles (e.g., `PROJECT_READER`) and custom roles (UUID-based)
- Pagination support for organizations with many custom roles


### Get Issues by Account
**Query File:** [`get_issues_by_account.graphql`](./get_issues_by_account.graphql)
Retrieves security issues for a specific cloud account. Returns open and in-progress issues grouped by severity. Essential for pre-deployment security reviews and ongoing security posture monitoring.

**Key Features:**
- Returns only OPEN and IN_PROGRESS issues
- Includes severity counts for quick overview (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
- Shows affected resource details (name, type, region, cloud platform)
- Returns control/policy information that triggered each issue
- Pagination support with `first: 100` results per query

**Variables:**
```json
{
  "subscriptionId": ["12345678-1234-1234-1234-123456789012"]
}
```