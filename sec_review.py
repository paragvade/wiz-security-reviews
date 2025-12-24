"""
Wiz Security Review Script
Automates cloud security posture reviews using Wiz GraphQL API
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
WIZ_CLIENT_ID = os.getenv("WIZ_CLIENT_ID")
WIZ_CLIENT_SECRET = os.getenv("WIZ_CLIENT_SECRET")
WIZ_API_URL = os.getenv("WIZ_API_URL")
WIZ_AUTH_URL = os.getenv("WIZ_AUTH_URL")


def get_token():
    """Authenticate and get access token"""
    response = requests.post(
        WIZ_AUTH_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": WIZ_CLIENT_ID,
            "client_secret": WIZ_CLIENT_SECRET,
            "audience": "wiz-api"
        },
        verify=False 
    )
    response.raise_for_status()
    return response.json()["access_token"]

def check_token_scopes(token):
    """Debug: Check what scopes the token has"""
    import base64
    import json
    
    # Decode JWT payload (middle part)
    parts = token.split('.')
    if len(parts) >= 2:
        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        decoded = base64.b64decode(payload)
        data = json.loads(decoded)
        print(f"Token scopes: {data.get('scope', 'No scopes found')}")


def run_query(token, query, variables=None):
    """Execute GraphQL query"""
    response = requests.post(
        WIZ_API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={"query": query, "variables": variables or {}},
        verify=False
    )
    response.raise_for_status()
    result = response.json()
    
    if "errors" in result:
        raise Exception(f"GraphQL Error: {result['errors']}")
    
    return result.get("data", {})


def get_cloud_account_id(token, external_id):
    """Get Wiz internal ID from AWS account ID or Azure subscription ID"""
    query = """
    query GetCloudAccount($externalId: [String!]) {
      cloudAccounts(first: 10, filterBy: {search: $externalId}) {
        nodes {
          id
          name
          externalId
          cloudProvider
        }
      }
    }
    """
    result = run_query(token, query, {"externalId": [external_id]})
    accounts = result.get("cloudAccounts", {}).get("nodes", [])
    
    # Find exact match
    for acc in accounts:
        if acc.get("externalId") == external_id:
            return acc
    
    return None


def get_issues(token, subscription_id):
    """Get all issues for a cloud account"""
    query = """
    query GetIssuesByAccount($subscriptionId: [String!]) {
      issuesV2(
        first: 100
        filterBy: {
          status: [OPEN, IN_PROGRESS]
          relatedEntity: {
            subscriptionId: $subscriptionId
          }
        }
      ) {
        nodes {
          id
          severity
          status
          createdAt
          sourceRule {
            ... on Control {
              name
              description
            }
          }
          entitySnapshot {
            name
            type
            nativeType
            cloudPlatform
            region
            subscriptionExternalId
          }
        }
        totalCount
        criticalSeverityCount
        highSeverityCount
        mediumSeverityCount
        lowSeverityCount
        informationalSeverityCount
      }
    }
    """
    return run_query(token, query, {"subscriptionId": [subscription_id]})


def print_summary(account_info, issues_data):
    """Print a summary of the security review"""
    issues = issues_data.get("issuesV2", {})
    
    print("\n" + "=" * 60)
    print("SECURITY REVIEW SUMMARY")
    print("=" * 60)
    print(f"Account Name:  {account_info.get('name')}")
    print(f"Account ID:    {account_info.get('externalId')}")
    print(f"Cloud:         {account_info.get('cloudProvider')}")
    print("=" * 60)
    print(f"Total Issues:  {issues.get('totalCount', 0)}")
    print("-" * 30)
    print(f"  CRITICAL:      {issues.get('criticalSeverityCount', 0)}")
    print(f"  HIGH:          {issues.get('highSeverityCount', 0)}")
    print(f"  MEDIUM:        {issues.get('mediumSeverityCount', 0)}")
    print(f"  LOW:           {issues.get('lowSeverityCount', 0)}")
    print(f"  INFORMATIONAL: {issues.get('informationalSeverityCount', 0)}")
    print("=" * 60)


def main():
    # Get account ID from user
    account_id = input("Enter AWS Account ID or Azure Subscription ID: ").strip()
    
    print("\nAuthenticating with Wiz...")
    token = get_token()
    print("Authentication successful!")

    check_token_scopes(token)
    
    print(f"\nLooking up account: {account_id}")
    account_info = get_cloud_account_id(token, account_id)
    
    if not account_info:
        print(f"Error: Account {account_id} not found in Wiz")
        return
    
    print(f"Found: {account_info.get('name')} ({account_info.get('cloudProvider')})")
    
    print("\nFetching issues...")
    issues_data = get_issues(token, account_info["id"])
    
    print_summary(account_info, issues_data)


if __name__ == "__main__":
    main()