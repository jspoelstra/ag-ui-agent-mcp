# AG-UI Agent with MCP on Azure Foundry

A complete example of creating an agent using Microsoft Agent Framework (MAF), with access to MCP (Model Context Protocol) tools, deployed as a **hosted agent on Azure AI Foundry**, that exposes the AG-UI protocol.

> **📖 New to this implementation?** See [AG_UI_AND_FOUNDRY_EXPLAINED.md](./AG_UI_AND_FOUNDRY_EXPLAINED.md) for detailed explanations of how AG-UI support and Azure Foundry deployment work in this code.

## Overview

This repository demonstrates:
- ✅ **Agent Creation**: Using Microsoft Agent Framework (MAF) to create an intelligent agent
- ✅ **MCP Integration**: Connecting to knowledge sources via Model Context Protocol
- ✅ **AG-UI Endpoint**: Exposing the agent via AG-UI protocol for frontend integration
- ✅ **Foundry Hosted Deployment**: Deploying as a fully managed agent on Azure AI Foundry
- ✅ **Production Ready**: Complete with infrastructure-as-code and deployment scripts

## Key Concepts

### Foundry v2 Hosted Agent Deployment
This repository uses **Foundry v2 hosted agent deployment** where the agent runs on Foundry's managed infrastructure, not locally or in containers you manage. Benefits include:
- **Fully Managed**: Foundry handles infrastructure, scaling, and monitoring
- **One-Command Deployment**: Use `azd up` to deploy everything
- **Enterprise-Ready**: Built-in security, compliance, and governance
- **Auto-Scaling**: Automatically scales from 1-10 instances based on demand

See [detailed explanation](./AG_UI_AND_FOUNDRY_EXPLAINED.md#foundry-v2-hosted-agent-deployment-recommended).

### AG-UI Support
This code **HAS full AG-UI support** via the `agent-framework-ag-ui` package. The function `add_agent_framework_fastapi_endpoint()` IS how AG-UI protocol endpoints are exposed in the Microsoft Agent Framework. See [detailed explanation](./AG_UI_AND_FOUNDRY_EXPLAINED.md#1-ag-ui-support---why-add_agent_framework_fastapi_endpoint).

## Features

- **Intake Form Assistant**: Helps users complete intake forms with access to knowledge base
- **Knowledge Base Access**: Connects to Azure AI Search via MCP for project information
- **AG-UI Protocol**: Exposes standard AG-UI endpoint for frontend frameworks (CopilotKit, etc.)
- **Foundry Hosted**: Deployed as a managed service on Azure AI Foundry
- **Auto-Scaling**: Automatically scales from 1-10 instances based on demand
- **Integrated Monitoring**: Built-in Application Insights and logging

## Quick Start

### Prerequisites

- **Azure Developer CLI (azd)**: Version 1.23.0 or later
  - macOS/Linux: `curl -fsSL https://aka.ms/install-azd.sh | bash`
  - Windows: `winget install microsoft.azd`
- **Docker Desktop**: For building container images
- **Azure CLI**: For authentication (`az login`)
- **Azure subscription**: With AI Foundry access
- **Python 3.11+**: For local development (optional)

### Deployment to Foundry (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/jspoelstra/ag-ui-agent-mcp.git
   cd ag-ui-agent-mcp
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Login to Azure**
   ```bash
   az login
   ```

4. **Deploy to Foundry**
   ```bash
   # Initialize deployment (first time only)
   azd init
   
   # Deploy everything (infrastructure + agent)
   azd up
   ```

   This single command will:
   - Provision Azure AI Foundry project
   - Build and push Docker image
   - Deploy agent as a hosted service
   - Configure auto-scaling and monitoring
   - Expose AG-UI endpoint

5. **View deployment**
   ```bash
   # Check agent status
   azd ai agent show
   
   # View logs
   azd monitor --logs
   ```

The AG-UI endpoint will be available at the Foundry-provided URL.

### Local Development (Optional)

For development and testing, you can run the agent locally:

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure AI Project endpoint
   ```

3. **Run locally**
   ```bash
   python agent.py
   ```

   The AG-UI endpoint will be available at `http://localhost:8000/`

   **Note**: In local mode, the agent runs on your machine but connects to Foundry for models and tools.

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required: Azure AI Project endpoint (recommended) or connection string
PROJECT_ENDPOINT=<your-project-endpoint-url>
# Example: https://your-project-name.region.inference.ai.azure.com

# Alternative (legacy): Use connection string instead of endpoint
# AZURE_AI_PROJECT_CONNECTION_STRING=<your-connection-string>

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
├── agent.yaml            # Agent definition for Foundry deployment
├── azure.yaml            # Azure Developer CLI configuration
├── infra/                # Infrastructure as Code (Bicep templates)
│   ├── main.bicep        # Main infrastructure deployment
│   └── foundry-project.bicep  # AI Foundry project resources
├── agent.py              # Agent implementation (for local dev)
├── deploy.py             # Deployment helper script
├── Dockerfile            # Container image definition
├── requirements.txt      # Python dependencies
├── .env.example          # Environment configuration template
└── README.md             # This file
```

## Deployment Architecture

### Foundry Hosted Deployment (Recommended)

```
Developer Machine
       ↓
    azd up
       ↓
┌──────────────────────────────────────────┐
│  Azure AI Foundry (Managed Platform)     │
│  ├─ Container Registry (agent image)     │
│  ├─ Hosted Agent Service (runs agent)    │
│  ├─ Auto-Scaling (1-10 instances)        │
│  ├─ Load Balancing                       │
│  ├─ AG-UI Endpoint (exposed)             │
│  └─ Monitoring & Logs                    │
└──────────────────────────────────────────┘
       ↓
Frontend/Clients → https://[foundry-endpoint]/agents/IntakeFormAssistant
```

### Self-Hosted Development (Optional)

```
┌──────────────────────────────────┐
│  Your Infrastructure             │
│  ├─ Local/Container (agent.py)   │
│  ├─ FastAPI (AG-UI endpoint)     │
│  └─ You manage scaling/monitoring│
└─────────────┬────────────────────┘
              │ CONNECTION_STRING
              ↓
┌──────────────────────────────────┐
│  Azure AI Project (Foundry)      │
│  ├─ Models (GPT-5-mini, etc.)    │
│  ├─ MCP Tools                    │
│  └─ Enterprise Security          │
└──────────────────────────────────┘
```

## Deployment

### Option 1: Deploy to Foundry (Recommended for Production)

Deploy as a fully managed agent on Azure AI Foundry:

```bash
# First time setup
azd init

# Deploy everything
azd up

# Check deployment status
azd ai agent show

# View logs
azd monitor --logs

# Update deployment
azd deploy
```

**What happens:**
- ✅ Provisions Azure AI Foundry project
- ✅ Builds and pushes Docker image
- ✅ Deploys agent as hosted service
- ✅ Configures auto-scaling (1-10 instances)
- ✅ Sets up monitoring and logging
- ✅ Exposes AG-UI endpoint

### Option 2: Validate Configuration

Check deployment prerequisites:

```bash
python deploy.py
```

This validates:
- Azure CLI is installed
- You're authenticated to Azure
- Required files are present
- Configuration is valid

### Option 3: Local Development

Run agent locally for development:

```bash
# Install dependencies
pip install -r requirements.txt

# Run agent
python agent.py
```

Agent will run at `http://localhost:8000/` and connect to Foundry for models.

### Option 4: Docker (Self-Managed)

For custom container deployments:

```bash
# Build image
docker build -t ag-ui-agent-mcp .

# Run container
docker run -p 8000:8000 --env-file .env ag-ui-agent-mcp
```

Deploy to Azure Container Apps or App Service as needed.

## Usage

### Testing the Deployed Agent

Once deployed to Foundry:

```bash
# Get the agent endpoint from deployment
azd ai agent show

# Test the AG-UI endpoint
curl -X POST https://[foundry-endpoint]/agents/IntakeFormAssistant/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "messages": [
      {"role": "user", "content": "Help me with an intake form"}
    ]
  }'
```

### Testing Local Agent

If running locally:

```bash
# Test the AG-UI endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
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
   - Verify your Azure AI Project endpoint or connection string is correct
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
