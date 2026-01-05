This document contains detailed documentation for all GraphQL queries used in the Wiz security review automation.

**Table of Contents**
- [Get Role Permissions](#get-role-permissions)
- [Get Cloud Accounts](#get-cloud-accounts)
- [Get Security Issues](#get-security-issues)
- [Get Vulnerabilities](#get-vulnerabilities)
- [Get Secrets](#get-secrets)

---

## Get Role Permissions

### Overview
Retrieves detailed permissions (scopes) for a specific Wiz role.

### Query File
[`queries/roles.graphql`](../queries/roles.graphql)

### GraphQL Query
```graphql
query GetRoleById($roleId: ID!) {
  userRole(id: $roleId) {
    id
    name
    description
    scopes
  }
}
```

### Variables
```json
{
  "roleId": "PROJECT_READER"
}
```

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `roleId` | `ID!` | Yes | Role identifier (string for built-in, UUID for custom) |

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Role identifier |
| `name` | String | Display name |
| `description` | String | Role purpose/description |
| `scopes` | Array | List of permission strings |
