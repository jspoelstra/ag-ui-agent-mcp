"""
Complete Python script using MAF (Microsoft Agent Framework) for creating and 
deploying an agent in Foundry (on Azure) that exposes an AG-UI endpoint and 
connects to a knowledge source via MCP (Model Context Protocol).

This script creates an agent with the following capabilities:
- Connects to MCP-based knowledge base tools
- Exposes AG-UI protocol endpoint for frontend integration
- Deploys on Azure Foundry platform
- Uses GPT-5-mini model for agent reasoning

KEY CONCEPTS EXPLAINED:

1. AG-UI SUPPORT:
   - This code HAS AG-UI support via the agent-framework-ag-ui package
   - The function add_agent_framework_fastapi_endpoint() IS how AG-UI is exposed
   - It's not a separate integration - this function adds AG-UI protocol endpoints to FastAPI
   - Frontend clients (CopilotKit, etc.) can connect via the AG-UI protocol

2. AZURE FOUNDRY DEPLOYMENT:
   - This code IS configured for Azure Foundry via AzureAIProjectAgentProvider
   - When you use this provider, your agent runs within Azure AI Project infrastructure
   - The AZURE_AI_PROJECT_CONNECTION_STRING connects to your Foundry project
   - Benefits: managed models, enterprise security, integrated monitoring, scalability

See AG_UI_AND_FOUNDRY_EXPLAINED.md for detailed explanations.
"""

import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from agent_framework import Agent

# AG-UI Support: This import from agent-framework-ag-ui package provides the
# add_agent_framework_fastapi_endpoint() function which IS how AG-UI protocol
# endpoints are exposed in the Microsoft Agent Framework
from agent_framework.ag_ui import add_agent_framework_fastapi_endpoint
from agent_framework.ag_ui.tools import HostedMCPTool

# Azure Foundry Deployment: This provider connects your agent to Azure AI Project
# (Foundry) infrastructure, enabling enterprise-grade managed deployment
from agent_framework.azure import AzureAIProjectAgentProvider

# Load environment variables
load_dotenv()


async def create_agent_with_mcp() -> Agent:
    """
    Create an agent with MCP tool connection to knowledge base.
    
    Returns:
        Agent: Configured agent instance with MCP tools
    """
    # Define MCP tool for knowledge base access
    # This connects to the Azure AI Search knowledge base via MCP
    mcp_kb_tool = HostedMCPTool(
        name="kb_kb_archive_f1nat",
        description="Access to knowledge base containing project information for intake form assistance",
        url=os.getenv(
            "MCP_SERVER_URL",
            "https://aisearch-nv-eastus2-dev-01.search.windows.net/knowledgebases/kb-archive/mcp?api-version=2025-11-01-Preview"
        ),
        approval_mode="never",  # Corresponds to require_approval: never in YAML
        # project_connection_id would be handled by the Azure AI Project context
    )
    
    # Create agent using Azure AI Project provider
    # AZURE FOUNDRY DEPLOYMENT: This is where the agent is deployed to Foundry!
    # - AzureAIProjectAgentProvider connects to Azure AI Project (Foundry)
    # - Uses AZURE_AI_PROJECT_CONNECTION_STRING for authentication
    # - The agent is provisioned within Foundry infrastructure
    # - Benefits: managed models, enterprise security, scalability, monitoring
    async with AzureAIProjectAgentProvider() as provider:
        agent = await provider.create_agent(
            name="IntakeFormAssistant",
            model=os.getenv("AGENT_MODEL", "gpt-5-mini"),
            instructions="""## Role
You are assisting users complete an intake form and have access to a knowledge
base that contains project information.""",
            description="Agent that assists with intake forms using knowledge base access via MCP",
            tools=[mcp_kb_tool],  # Attach MCP tool for knowledge base
        )
        return agent


def create_fastapi_app(agent: Agent) -> FastAPI:
    """
    Create FastAPI application with AG-UI endpoint.
    
    Args:
        agent: Configured agent instance
        
    Returns:
        FastAPI: Application with AG-UI endpoint configured
    """
    app = FastAPI(
        title="Intake Form Assistant Agent",
        description="AG-UI enabled agent with MCP knowledge base access",
        version="1.0.0"
    )
    
    # Add AG-UI endpoint at root path
    # AG-UI SUPPORT: This function from agent-framework-ag-ui package exposes
    # the AG-UI protocol endpoints, enabling frontend integration with:
    # - CopilotKit and other AG-UI clients
    # - Streaming responses via server-sent events
    # - Tool execution transparency
    # - Rich UI components support
    # This IS the AG-UI integration - add_agent_framework_fastapi_endpoint()
    # is the official way to expose AG-UI endpoints in the Microsoft Agent Framework
    add_agent_framework_fastapi_endpoint(app, agent, "/")
    
    return app


async def main():
    """
    Main entry point for creating and running the agent server.
    """
    print("Creating agent with MCP knowledge base connection...")
    agent = await create_agent_with_mcp()
    print(f"Agent created: {agent.name}")
    
    print("Setting up FastAPI app with AG-UI endpoint...")
    app = create_fastapi_app(agent)
    print("FastAPI app configured")
    
    # Configuration for uvicorn server
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"\nStarting AG-UI endpoint server on {host}:{port}")
    print(f"AG-UI endpoint available at: http://{host}:{port}/")
    print("\nAgent is ready to assist with intake forms using knowledge base!")
    
    # Import and run uvicorn
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    asyncio.run(main())
