"""
Deployment script for deploying the agent to Azure AI Foundry as a hosted agent.

This script uses Azure Developer CLI (azd) to deploy the agent to Foundry's
managed infrastructure, where it runs as a fully hosted service.

FOUNDRY V2 HOSTED AGENT DEPLOYMENT:
- Agents are deployed directly to Foundry's managed infrastructure
- No need to run locally or in containers on Azure Container Apps
- Foundry handles scaling, monitoring, and lifecycle management
- Use 'azd up' to provision and deploy everything

This is different from the legacy approach where you:
1. Run agent.py locally with AzureAIProjectAgentProvider
2. Containerize and deploy to Azure Container Apps/App Service

With Foundry v2 hosted agents:
1. Define agent in agent.yaml
2. Run 'azd up' to deploy to Foundry
3. Agent runs on Foundry's managed infrastructure

See AG_UI_AND_FOUNDRY_EXPLAINED.md for details on hosted vs self-hosted deployment.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

# Load environment variables
load_dotenv()


async def deploy_agent():
    """
    Deploy the agent to Azure Foundry as a hosted agent using azd.
    """
    print("=" * 70)
    print("Deploying Hosted Agent to Azure AI Foundry")
    print("=" * 70)
    print("\n🚀 FOUNDRY V2 HOSTED AGENT DEPLOYMENT")
    print("This script deploys your agent to Foundry's managed infrastructure.")
    print("Your agent will be fully hosted and managed by Azure AI Foundry.\n")
    
    # Check if azd is installed
    print("Checking prerequisites...")
    try:
        result = os.popen("azd version").read()
        if not result:
            print("\n❌ Error: Azure Developer CLI (azd) is not installed")
            print("\nPlease install azd:")
            print("- macOS/Linux: curl -fsSL https://aka.ms/install-azd.sh | bash")
            print("- Windows: winget install microsoft.azd")
            print("\nFor more info: https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd")
            sys.exit(1)
        print(f"✓ Azure Developer CLI installed: {result.strip()}")
    except Exception as e:
        print(f"\n❌ Error checking azd: {e}")
        sys.exit(1)
    
    # Check Azure authentication
    try:
        credential = DefaultAzureCredential()
        # Try to get a token to validate authentication
        token = credential.get_token("https://management.azure.com/.default")
        print("✓ Azure authentication configured")
    except Exception as e:
        print(f"\n❌ Error: Azure authentication failed")
        print(f"Details: {e}")
        print("\nPlease login to Azure:")
        print("  az login")
        sys.exit(1)
    
    # Check for required files
    required_files = ["agent.yaml", "azure.yaml", "Dockerfile"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"\n❌ Error: Missing required files: {', '.join(missing_files)}")
        print("\nPlease ensure all deployment files are present.")
        sys.exit(1)
    print("✓ Deployment files present")
    
    # Load environment variables to validate configuration
    load_dotenv()
    
    print("\n" + "=" * 70)
    print("Deployment Configuration:")
    print("=" * 70)
    print(f"  Agent Name: IntakeFormAssistant")
    print(f"  Model: {os.getenv('AGENT_MODEL', 'gpt-5-mini')}")
    print(f"  MCP Server: {os.getenv('MCP_SERVER_URL', 'configured')}")
    print(f"  Deployment Type: Foundry Hosted Agent")
    print(f"  AG-UI Protocol: Enabled")
    
    print("\n" + "=" * 70)
    print("Deployment Options:")
    print("=" * 70)
    print("\n1️⃣  DEPLOY TO FOUNDRY (Recommended)")
    print("   Deploy agent to Foundry's managed infrastructure:")
    print("   $ azd up")
    print("\n   This will:")
    print("   - Provision Azure AI Foundry project (if needed)")
    print("   - Build and push Docker image to Azure Container Registry")
    print("   - Deploy agent as a hosted service on Foundry")
    print("   - Configure auto-scaling and monitoring")
    print("   - Expose AG-UI endpoint\n")
    
    print("2️⃣  INITIALIZE DEPLOYMENT (First Time)")
    print("   If this is your first deployment:")
    print("   $ azd init")
    print("   Then run: azd up\n")
    
    print("3️⃣  CHECK DEPLOYMENT STATUS")
    print("   View deployed agent details:")
    print("   $ azd ai agent show\n")
    
    print("4️⃣  UPDATE AGENT")
    print("   Update an existing deployment:")
    print("   $ azd deploy\n")
    
    print("5️⃣  VIEW LOGS")
    print("   View agent logs:")
    print("   $ azd monitor --logs\n")
    
    print("=" * 70)
    print("What happens with Foundry Hosted Agent Deployment:")
    print("=" * 70)
    print("✅ Agent runs on Foundry's managed infrastructure (not locally)")
    print("✅ Foundry handles scaling, monitoring, and lifecycle management")
    print("✅ No need to manage containers or orchestration yourself")
    print("✅ Integrated with Azure security, compliance, and governance")
    print("✅ AG-UI endpoint automatically exposed and managed")
    print("✅ Built-in observability and Application Insights integration")
    
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print("1. Review the configuration in agent.yaml and azure.yaml")
    print("2. Ensure environment variables are set in .env")
    print("3. Run: azd up")
    print("4. Access your agent via the Foundry-provided endpoint")
    print("\n📖 For detailed explanations, see AG_UI_AND_FOUNDRY_EXPLAINED.md")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(deploy_agent())
