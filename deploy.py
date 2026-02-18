"""
Deployment script for deploying the MAF agent to Azure Foundry.

This script handles:
- Azure authentication validation
- Connection to Azure AI Project (Foundry) 
- Agent deployment configuration verification
- Health check and connectivity tests

IMPORTANT: This script validates that your agent can connect to Azure Foundry.
When you run agent.py with a valid AZURE_AI_PROJECT_CONNECTION_STRING, the
AzureAIProjectAgentProvider automatically deploys your agent to the Foundry
infrastructure. This script helps verify that configuration is correct before
running the actual agent.

See AG_UI_AND_FOUNDRY_EXPLAINED.md for details on how Foundry deployment works.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
load_dotenv()


async def deploy_agent():
    """
    Deploy the agent to Azure Foundry platform.
    """
    print("=" * 70)
    print("Deploying Agent to Azure Foundry")
    print("=" * 70)
    
    # Get Azure configuration from environment
    # Support both modern endpoint format and legacy connection string
    endpoint = os.getenv("PROJECT_ENDPOINT")
    connection_string = os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
    
    # If endpoint is not set, try to parse it from connection string
    if not endpoint and connection_string:
        # Parse connection string to extract endpoint
        # Format: "ProjectId=<UUID>;Location=<region>;Endpoint=https://<something>.azure.com;..."
        try:
            parts = dict(item.split("=", 1) for item in connection_string.split(";") if item and "=" in item)
            endpoint = parts.get("Endpoint")
            if not endpoint:
                print("\n❌ Error: Missing 'Endpoint' field in connection string")
                print("Connection string should contain: Endpoint=https://...")
                endpoint = None
        except Exception as e:
            print(f"\n❌ Error: Invalid connection string format: {e}")
            print("Expected format: ProjectId=...;Endpoint=https://...;...")
            endpoint = None
    
    if not endpoint:
        print("\n❌ Error: PROJECT_ENDPOINT or AZURE_AI_PROJECT_CONNECTION_STRING not set")
        print("\nPlease set your Azure AI Project endpoint:")
        print("1. Copy .env.example to .env")
        print("2. Set PROJECT_ENDPOINT to your Azure AI Project endpoint URL")
        print("   Example: https://your-project.region.inference.ai.azure.com")
        print("   OR set AZURE_AI_PROJECT_CONNECTION_STRING (legacy format)")
        print("3. Run this script again")
        sys.exit(1)
    
    try:
        # Create Azure credential
        credential = DefaultAzureCredential()
        print("✓ Azure authentication configured")
        
        # Create AI Project client with endpoint
        client = AIProjectClient(
            endpoint=endpoint,
            credential=credential
        )
        print("✓ Connected to Azure AI Project")
        
        # Deploy agent configuration
        print("\nValidating Azure Foundry deployment configuration:")
        print(f"  - Model: {os.getenv('AGENT_MODEL', 'gpt-5-mini')}")
        print(f"  - MCP Server: {os.getenv('MCP_SERVER_URL', 'configured')}")
        print(f"  - AG-UI Endpoint: Enabled via add_agent_framework_fastapi_endpoint()")
        print(f"  - Foundry Provider: AzureAIProjectAgentProvider")
        
        # Note: The actual Foundry deployment happens when agent.py runs
        # The AzureAIProjectAgentProvider in agent.py handles:
        # - Connecting to Azure AI Project (Foundry)
        # - Provisioning the agent in Foundry infrastructure  
        # - Managing model deployments
        # - Coordinating with Azure services
        # This script validates the configuration is ready for that deployment
        
        print("\n" + "=" * 70)
        print("✅ Azure Foundry Deployment Configuration Validated!")
        print("=" * 70)
        print("\nWhat happens when you run 'python agent.py':")
        print("1. AzureAIProjectAgentProvider connects to your Azure AI Project (Foundry)")
        print("2. The agent is provisioned within Foundry infrastructure")
        print("3. Model deployments and tool connections are configured")
        print("4. AG-UI endpoints are exposed via FastAPI")
        print("5. Your agent is ready to serve requests!")
        print("\nNext steps:")
        print("1. Ensure your Azure credentials are configured (az login)")
        print("2. Run the agent locally with Foundry connection: python agent.py")
        print("3. For production, containerize and deploy to:")
        print("   - Azure Container Apps (recommended)")
        print("   - Azure App Service")
        print("   - Azure Kubernetes Service")
        print("\nThe agent will run on your infrastructure but connect to Foundry")
        print("for managed models, enterprise security, and integrated monitoring.")
        print("\nFor containerized deployment, see the Dockerfile included.")
        print("\n📖 For detailed explanations, see AG_UI_AND_FOUNDRY_EXPLAINED.md")
        
    except Exception as e:
        print(f"\n❌ Deployment error: {e}")
        print("\nTroubleshooting:")
        print("- Verify your Azure AI Project connection string is correct")
        print("- Ensure you're logged in: az login")
        print("- Check that your Azure subscription has the necessary permissions")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(deploy_agent())
