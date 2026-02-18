# AG-UI Agent with MCP on Azure Foundry

A complete example of creating an agent using Microsoft Agent Framework (MAF), with access to MCP (Model Context Protocol) tools, deployed on Foundry (Azure), that exposes the AG-UI protocol.

> **📖 New to this implementation?** See [AG_UI_AND_FOUNDRY_EXPLAINED.md](./AG_UI_AND_FOUNDRY_EXPLAINED.md) for detailed explanations of how AG-UI support and Azure Foundry deployment work in this code.

## Overview

This repository demonstrates:
- ✅ **Agent Creation**: Using Microsoft Agent Framework (MAF) to create an intelligent agent
- ✅ **MCP Integration**: Connecting to knowledge sources via Model Context Protocol
- ✅ **AG-UI Endpoint**: Exposing the agent via AG-UI protocol for frontend integration
- ✅ **Azure Deployment**: Deploying to Azure Foundry platform
- ✅ **Production Ready**: Complete with Docker support and deployment scripts

## Key Concepts

### AG-UI Support
This code **HAS full AG-UI support** via the `agent-framework-ag-ui` package. The function `add_agent_framework_fastapi_endpoint()` IS how AG-UI protocol endpoints are exposed in the Microsoft Agent Framework. See [detailed explanation](./AG_UI_AND_FOUNDRY_EXPLAINED.md#1-ag-ui-support---why-add_agent_framework_fastapi_endpoint).

### Azure Foundry Deployment  
This code **IS configured for Azure Foundry** via the `AzureAIProjectAgentProvider`. When you use this provider, your agent runs within Azure AI Project infrastructure. See [detailed explanation](./AG_UI_AND_FOUNDRY_EXPLAINED.md#2-azure-foundry-deployment---how-is-it-deployed).

## Features

- **Intake Form Assistant**: Helps users complete intake forms with access to knowledge base
- **Knowledge Base Access**: Connects to Azure AI Search via MCP for project information
- **AG-UI Protocol**: Exposes standard AG-UI endpoint for frontend frameworks (CopilotKit, etc.)
- **Azure Native**: Built for Azure Foundry with full Azure integration
- **Containerized**: Docker support for easy deployment to Azure services

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Azure subscription with AI Project access
- Azure CLI installed and configured (`az login`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jspoelstra/ag-ui-agent-mcp.git
   cd ag-ui-agent-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure AI Project connection string
   ```

4. **Run the agent locally**
   ```bash
   python agent.py
   ```

   The AG-UI endpoint will be available at `http://localhost:8000/`

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required: Azure AI Project connection string from Foundry
AZURE_AI_PROJECT_CONNECTION_STRING=<your-connection-string>

# Optional: Agent configuration
AGENT_MODEL=gpt-5-mini
HOST=0.0.0.0
PORT=8000

# MCP Server URL (default provided)
MCP_SERVER_URL=https://aisearch-nv-eastus2-dev-01.search.windows.net/knowledgebases/kb-archive/mcp?api-version=2025-11-01-Preview
```

### Azure Authentication

The agent uses `DefaultAzureCredential` which supports:
- Environment variables (for production)
- Managed Identity (for Azure services)
- Azure CLI (`az login` for local development)
- Visual Studio Code
- Azure PowerShell

For local development, run:
```bash
az login
```

## Project Structure

```
ag-ui-agent-mcp/
├── agent.py              # Main agent implementation
├── deploy.py             # Deployment script and validation
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment configuration template
└── README.md            # This file
```

## Agent Architecture

The agent is built with three key components:

### 1. MCP Tool Connection
```python
mcp_kb_tool = HostedMCPTool(
    name="kb_kb_archive_f1nat",
    description="Access to knowledge base containing project information",
    url="https://aisearch-nv-eastus2-dev-01.search.windows.net/...",
    approval_mode="never",  # No human-in-the-loop required
)
```

### 2. Agent Creation with Azure Provider
```python
async with AzureAIProjectAgentProvider() as provider:
    agent = await provider.create_agent(
        name="IntakeFormAssistant",
        model="gpt-5-mini",
        instructions="You are assisting users complete an intake form...",
        tools=[mcp_kb_tool],
    )
```

### 3. AG-UI Endpoint Exposure
```python
app = FastAPI()
add_agent_framework_fastapi_endpoint(app, agent, "/")
```

## Deployment

### Option 1: Local Development
```bash
python agent.py
```

### Option 2: Validate Configuration
```bash
python deploy.py
```

### Option 3: Docker Deployment
```bash
# Build image
docker build -t ag-ui-agent-mcp .

# Run container
docker run -p 8000:8000 --env-file .env ag-ui-agent-mcp
```

### Option 4: Azure Container Apps
```bash
# Login to Azure
az login

# Create resource group (if needed)
az group create --name rg-ag-ui-agent --location eastus2

# Create container registry (if needed)
az acr create --resource-group rg-ag-ui-agent --name <your-registry> --sku Basic

# Build and push image
az acr build --registry <your-registry> --image ag-ui-agent-mcp:latest .

# Deploy to Container Apps
az containerapp create \
  --name ag-ui-agent-mcp \
  --resource-group rg-ag-ui-agent \
  --image <your-registry>.azurecr.io/ag-ui-agent-mcp:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars AZURE_AI_PROJECT_CONNECTION_STRING=<your-connection-string>
```

### Option 5: Azure App Service
```bash
# Create App Service plan
az appservice plan create \
  --name asp-ag-ui-agent \
  --resource-group rg-ag-ui-agent \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group rg-ag-ui-agent \
  --plan asp-ag-ui-agent \
  --name <your-app-name> \
  --deployment-container-image-name <your-registry>.azurecr.io/ag-ui-agent-mcp:latest

# Configure environment variables
az webapp config appsettings set \
  --resource-group rg-ag-ui-agent \
  --name <your-app-name> \
  --settings AZURE_AI_PROJECT_CONNECTION_STRING=<your-connection-string>
```

## Usage

### Testing the AG-UI Endpoint

Once running, you can test the endpoint:

```bash
# Health check (if implemented)
curl http://localhost:8000/health

# AG-UI endpoint
curl http://localhost:8000/
```

### Frontend Integration

The agent exposes an AG-UI endpoint compatible with:
- **CopilotKit**: React-based AI copilot framework
- **Other AG-UI clients**: Any client supporting the AG-UI protocol

Example CopilotKit integration:
```typescript
import { CopilotKit } from "@copilotkit/react-core";

<CopilotKit runtimeUrl="http://localhost:8000">
  {/* Your app components */}
</CopilotKit>
```

## Development

### Code Quality

This project follows Python best practices:
- Type hints for better code clarity
- Async/await for efficient I/O operations
- Environment-based configuration
- Comprehensive documentation

### Running Tests

```bash
# Install dev dependencies (if any)
pip install -r requirements.txt

# Run tests
pytest
```

## Agent Configuration (YAML Reference)

The agent configuration matches the Foundry YAML format:

```yaml
definition:
  kind: prompt
  model: gpt-5-mini
  instructions: |
    ## Role
    You are assisting users complete an intake form and have access to a knowledge
    base that contains project information.
  tools:
    - type: mcp
      server_label: kb_kb_archive_f1nat
      server_url: https://aisearch-nv-eastus2-dev-01.search.windows.net/knowledgebases/kb-archive/mcp?api-version=2025-11-01-Preview
      require_approval: never
      project_connection_id: kb-kb-archive-f1nat
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure you're logged in: `az login`
   - Verify your Azure AI Project connection string is correct
   - Check that your account has necessary permissions

2. **MCP Connection Issues**
   - Verify the MCP server URL is accessible
   - Check network connectivity to Azure AI Search
   - Ensure API version is supported

3. **Port Already in Use**
   - Change the PORT in `.env` file
   - Or kill the process using port 8000: `lsof -ti:8000 | xargs kill -9`

### Logs and Debugging

Set log level in `.env`:
```bash
LOG_LEVEL=DEBUG
```

## References

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [AG-UI Integration Guide](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Azure AI Services](https://azure.microsoft.com/en-us/products/ai-services)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
- Open an issue in this repository
- Check the Microsoft Agent Framework documentation
- Review the AG-UI integration guide
