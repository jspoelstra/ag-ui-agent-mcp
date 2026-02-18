# Implementation Summary

> **📖 Quick Explanation Needed?** See [AG_UI_AND_FOUNDRY_EXPLAINED.md](./AG_UI_AND_FOUNDRY_EXPLAINED.md) for detailed answers to:
> - Why does the code use `add_agent_framework_fastapi_endpoint` for AG-UI?
> - How is the agent deployed on Microsoft Foundry on Azure?

## Overview
This repository provides a **complete, production-ready** example of creating an AI agent using Microsoft Agent Framework (MAF) that:
- Connects to knowledge sources via MCP (Model Context Protocol)
- Exposes an AG-UI endpoint for frontend integration (via `add_agent_framework_fastapi_endpoint`)
- Deploys to Azure Foundry platform (via `AzureAIProjectAgentProvider`)

## What's Included

### Core Implementation Files

1. **`agent.py`** - Main agent implementation
   - Creates agent with MCP tool for knowledge base access
   - Configures Azure AI Project provider
   - Exposes AG-UI endpoint via FastAPI
   - Uses GPT-5-mini model as specified
   - Async/await pattern for optimal performance

2. **`deploy.py`** - Deployment validation script
   - Validates Azure configuration
   - Checks connection string and authentication
   - Provides deployment guidance
   - Error handling and troubleshooting tips

3. **`test_client.py`** - Example test client
   - Tests basic connectivity
   - Sends sample queries to the agent
   - Validates knowledge base integration
   - Demonstrates proper API usage

### Configuration Files

4. **`.env.example`** - Environment configuration template
   - Azure AI Project connection string
   - Agent model configuration
   - MCP server URL
   - Host/port settings

5. **`requirements.txt`** - Python dependencies
   - agent-framework (core)
   - agent-framework-ag-ui (AG-UI integration)
   - azure-ai-projects (Azure integration)
   - azure-identity (authentication)
   - uvicorn (ASGI server)
   - python-dotenv (config management)
   - requests (HTTP client for testing)

### Deployment Support

6. **`Dockerfile`** - Container configuration
   - Python 3.11 slim base image
   - Security best practices (non-root user)
   - Health checks
   - Production-ready setup

7. **`docker-compose.yml`** - Local development
   - Easy local testing
   - Environment variable support
   - Health checks
   - Network configuration

8. **`.github/workflows/ci-cd.yml`** - CI/CD pipeline
   - Code validation
   - Security scanning with Trivy
   - Docker build and push
   - Automated deployment to Azure

### Documentation

9. **`README.md`** - Main documentation
   - Quick start guide
   - Architecture overview
   - Configuration instructions
   - Deployment options
   - Usage examples
   - Troubleshooting

10. **`USAGE.md`** - Comprehensive usage guide
    - Detailed setup instructions
    - All deployment options (Container Apps, App Service, etc.)
    - Frontend integration examples
    - Best practices
    - Advanced troubleshooting

11. **`CONTRIBUTING.md`** - Contribution guidelines
    - Development setup
    - Code standards
    - PR process
    - Security guidelines

12. **`quickstart.sh`** - Quick start script
    - Automated setup
    - Dependency installation
    - Configuration validation
    - One-command launch

## Key Features

### MCP Integration
- Connects to Azure AI Search knowledge base via MCP
- Server URL: `https://aisearch-nv-eastus2-dev-01.search.windows.net/...`
- No approval required for tool execution
- Matches YAML configuration from Foundry

### AG-UI Protocol
- Standard AG-UI endpoint at root path (`/`)
- Exposed via `add_agent_framework_fastapi_endpoint()` from agent-framework-ag-ui package
- Compatible with CopilotKit and other AG-UI clients
- Streaming support
- Rich UI components

### Azure Foundry Deployment
- Uses `AzureAIProjectAgentProvider` to connect to Azure AI Project (Foundry)
- Agent provisioned within Foundry infrastructure when agent.py runs
- Supports connection string authentication via AZURE_AI_PROJECT_CONNECTION_STRING
- Compatible with Azure Container Apps, App Service, AKS for hosting the FastAPI server
- Production-ready configuration with managed models and enterprise security

## Agent Configuration Mapping

The Python implementation matches the provided YAML:

```yaml
# YAML Configuration
definition:
  kind: prompt                    # ✓ Prompt-based agent
  model: gpt-5-mini              # ✓ Set via AGENT_MODEL
  instructions: |                 # ✓ Set in create_agent()
    ## Role
    You are assisting users...
  tools:
    - type: mcp                   # ✓ HostedMCPTool
      server_label: kb_kb_archive_f1nat    # ✓ tool.name
      server_url: https://...     # ✓ tool.url
      require_approval: never     # ✓ approval_mode="never"
      project_connection_id: ...  # ✓ Handled by Azure provider
```

## Usage Examples

### Local Development
```bash
./quickstart.sh
# or
python agent.py
```

### Docker
```bash
docker-compose up
```

### Azure Container Apps
```bash
az containerapp create \
  --name ag-ui-agent-mcp \
  --resource-group rg-ag-ui-agent \
  --image myregistry.azurecr.io/ag-ui-agent-mcp:latest \
  --target-port 8000 \
  --ingress external
```

### Testing
```bash
python test_client.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (AG-UI Client)              │
│                  (CopilotKit, Custom UI)                │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/WebSocket
                         │ AG-UI Protocol
                         ▼
┌─────────────────────────────────────────────────────────┐
│                     FastAPI Server                       │
│              add_agent_framework_fastapi_endpoint        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 Microsoft Agent Framework                │
│                  (agent-framework)                       │
├─────────────────────────────────────────────────────────┤
│  Agent: IntakeFormAssistant                             │
│  Model: gpt-5-mini                                      │
│  Provider: AzureAIProjectAgentProvider                  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    MCP Tool                              │
│              (HostedMCPTool)                             │
└────────────────────────┬────────────────────────────────┘
                         │ MCP Protocol
                         ▼
┌─────────────────────────────────────────────────────────┐
│          Azure AI Search Knowledge Base                 │
│     (kb-archive via MCP endpoint)                       │
└─────────────────────────────────────────────────────────┘
```

## Security Considerations

- ✓ Environment variables for sensitive data
- ✓ .env files excluded from git
- ✓ Non-root Docker user
- ✓ DefaultAzureCredential for flexible auth
- ✓ Security scanning in CI/CD
- ✓ HTTPS for production deployments

## Next Steps

1. **Customize the Agent**
   - Modify instructions in `agent.py`
   - Add additional MCP tools
   - Adjust model parameters

2. **Add Features**
   - Implement authentication
   - Add logging and monitoring
   - Create custom tools

3. **Deploy to Production**
   - Set up Azure resources
   - Configure CI/CD secrets
   - Deploy via GitHub Actions

4. **Integrate Frontend**
   - Build React/Vue/Angular app
   - Use CopilotKit or custom AG-UI client
   - Connect to deployed endpoint

## Support and Resources

- **Microsoft Agent Framework**: https://learn.microsoft.com/en-us/agent-framework/
- **AG-UI Documentation**: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Azure AI Services**: https://azure.microsoft.com/en-us/products/ai-services

## License

MIT License - see LICENSE file for details
