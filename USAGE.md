# Usage Guide for AG-UI Agent with MCP

This guide provides detailed instructions for setting up, running, and deploying the agent.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Setup](#local-setup)
3. [Running the Agent](#running-the-agent)
4. [Testing the Agent](#testing-the-agent)
5. [Deployment Options](#deployment-options)
6. [Frontend Integration](#frontend-integration)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- Python 3.11 or higher
- pip (Python package manager)
- Azure CLI (`az`)
- Docker (optional, for containerized deployment)

### Required Azure Resources
- Azure subscription
- Azure AI Project on Foundry platform
- Access to the MCP server URL (Azure AI Search knowledge base)

### Getting Your Azure AI Project Connection String

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Go to your Azure AI Project
3. Find the **Connection String** in the Overview or Settings section
4. Copy the connection string (format: `endpoint=https://...;key=...`)

## Local Setup

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/jspoelstra/ag-ui-agent-mcp.git
cd ag-ui-agent-mcp

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# Required: Set AZURE_AI_PROJECT_CONNECTION_STRING
# Optional: Customize other settings
```

Example `.env` file:
```bash
AZURE_AI_PROJECT_CONNECTION_STRING=endpoint=https://your-project.azure.com;key=YOUR_KEY
AGENT_MODEL=gpt-5-mini
HOST=0.0.0.0
PORT=8000
MCP_SERVER_URL=https://aisearch-nv-eastus2-dev-01.search.windows.net/knowledgebases/kb-archive/mcp?api-version=2025-11-01-Preview
```

### Step 3: Authenticate with Azure

```bash
# Login to Azure
az login

# Verify your subscription
az account show
```

## Running the Agent

### Option 1: Direct Python Execution

```bash
# Run the agent
python agent.py
```

Expected output:
```
Creating agent with MCP knowledge base connection...
Agent created: IntakeFormAssistant
Setting up FastAPI app with AG-UI endpoint...
FastAPI app configured

Starting AG-UI endpoint server on 0.0.0.0:8000
AG-UI endpoint available at: http://0.0.0.0:8000/

Agent is ready to assist with intake forms using knowledge base!
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Option 2: Using uvicorn Directly

```bash
# Run with custom settings
uvicorn agent:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reload during development.

## Testing the Agent

### Using the Test Client

```bash
# Run the test client
python test_client.py

# Or test a remote endpoint
python test_client.py https://your-agent.azurewebsites.net
```

### Using curl

```bash
# Test basic connectivity
curl http://localhost:8000/

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Hello! Can you help me with an intake form?"
      }
    ]
  }'
```

### Using Postman or Thunder Client

1. Create a new POST request
2. URL: `http://localhost:8000/chat`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What projects are available in the knowledge base?"
    }
  ]
}
```

## Deployment Options

### Validate Configuration First

Before deploying, validate your configuration:

```bash
python deploy.py
```

This script checks:
- Azure authentication
- Connection string validity
- MCP server accessibility
- Required environment variables

### Option 1: Azure Container Apps (Recommended)

**Advantages:**
- Serverless, auto-scaling
- Built-in HTTPS
- Easy management

**Steps:**

```bash
# 1. Login and set subscription
az login
az account set --subscription "Your Subscription Name"

# 2. Create resource group
az group create \
  --name rg-ag-ui-agent \
  --location eastus2

# 3. Create container registry
az acr create \
  --resource-group rg-ag-ui-agent \
  --name <your-unique-registry-name> \
  --sku Basic

# 4. Build and push image
az acr build \
  --registry <your-unique-registry-name> \
  --image ag-ui-agent-mcp:latest \
  .

# 5. Create container app environment
az containerapp env create \
  --name env-ag-ui-agent \
  --resource-group rg-ag-ui-agent \
  --location eastus2

# 6. Deploy container app
az containerapp create \
  --name ag-ui-agent-mcp \
  --resource-group rg-ag-ui-agent \
  --environment env-ag-ui-agent \
  --image <your-unique-registry-name>.azurecr.io/ag-ui-agent-mcp:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server <your-unique-registry-name>.azurecr.io \
  --env-vars \
    AZURE_AI_PROJECT_CONNECTION_STRING="<your-connection-string>" \
    AGENT_MODEL="gpt-5-mini" \
    MCP_SERVER_URL="<your-mcp-url>"

# 7. Get the URL
az containerapp show \
  --name ag-ui-agent-mcp \
  --resource-group rg-ag-ui-agent \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

### Option 2: Azure App Service

**Advantages:**
- Familiar PaaS experience
- Good for traditional web apps
- Built-in deployment slots

**Steps:**

```bash
# 1. Create App Service plan
az appservice plan create \
  --name asp-ag-ui-agent \
  --resource-group rg-ag-ui-agent \
  --sku B1 \
  --is-linux

# 2. Create Web App
az webapp create \
  --resource-group rg-ag-ui-agent \
  --plan asp-ag-ui-agent \
  --name <your-unique-app-name> \
  --deployment-container-image-name <your-registry>.azurecr.io/ag-ui-agent-mcp:latest

# 3. Configure environment variables
az webapp config appsettings set \
  --resource-group rg-ag-ui-agent \
  --name <your-unique-app-name> \
  --settings \
    AZURE_AI_PROJECT_CONNECTION_STRING="<your-connection-string>" \
    AGENT_MODEL="gpt-5-mini"

# 4. Enable managed identity for Azure auth
az webapp identity assign \
  --resource-group rg-ag-ui-agent \
  --name <your-unique-app-name>
```

### Option 3: Docker Compose (Local or VM)

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## Frontend Integration

### CopilotKit Integration

Install CopilotKit in your React app:

```bash
npm install @copilotkit/react-core @copilotkit/react-ui
```

Configure the provider:

```typescript
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";

function App() {
  return (
    <CopilotKit runtimeUrl="http://localhost:8000">
      <CopilotSidebar>
        <YourApp />
      </CopilotSidebar>
    </CopilotKit>
  );
}
```

### Custom AG-UI Client

For custom implementations, the AG-UI protocol supports:
- Standard chat messages
- Streaming responses
- Tool execution notifications
- Rich UI components

See the [AG-UI specification](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/) for details.

## Troubleshooting

### Common Issues

#### 1. "AZURE_AI_PROJECT_CONNECTION_STRING not set"

**Solution:**
```bash
# Ensure .env file exists and contains the connection string
cp .env.example .env
# Edit .env and add your connection string
```

#### 2. "Authentication failed"

**Solutions:**
```bash
# Re-login to Azure
az login

# Or set environment variables for service principal
export AZURE_CLIENT_ID="..."
export AZURE_TENANT_ID="..."
export AZURE_CLIENT_SECRET="..."
```

#### 3. "MCP server unreachable"

**Check:**
- Network connectivity to the MCP URL
- Firewall rules allow outbound HTTPS
- MCP server URL is correct
- API version is supported

**Test:**
```bash
curl -I "https://aisearch-nv-eastus2-dev-01.search.windows.net/knowledgebases/kb-archive/mcp?api-version=2025-11-01-Preview"
```

#### 4. "Port 8000 already in use"

**Solutions:**
```bash
# Option 1: Change port in .env
PORT=8001

# Option 2: Kill process using port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000    # Windows (then kill PID)
```

#### 5. "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or install specific package
pip install agent-framework-ag-ui
```

### Debugging Tips

1. **Enable debug logging:**
   ```bash
   # In .env
   LOG_LEVEL=DEBUG
   ```

2. **Check agent logs:**
   ```bash
   # Run with verbose output
   python agent.py 2>&1 | tee agent.log
   ```

3. **Test Azure connectivity:**
   ```bash
   az account show
   az rest --method get --url "https://management.azure.com/subscriptions?api-version=2020-01-01"
   ```

4. **Verify Docker build:**
   ```bash
   docker build -t ag-ui-agent-mcp .
   docker run --env-file .env -p 8000:8000 ag-ui-agent-mcp
   ```

### Getting Help

- **Microsoft Agent Framework Docs**: https://learn.microsoft.com/en-us/agent-framework/
- **AG-UI Documentation**: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/
- **Azure Support**: https://azure.microsoft.com/en-us/support/
- **GitHub Issues**: Open an issue in this repository

## Best Practices

### Security
- Never commit `.env` files to version control
- Use Azure Key Vault for production secrets
- Enable managed identity for Azure services
- Implement rate limiting for public endpoints

### Performance
- Use Azure Container Apps autoscaling
- Enable response caching when appropriate
- Monitor agent response times
- Optimize MCP queries

### Monitoring
- Enable Application Insights for Azure deployments
- Set up alerts for errors and performance
- Monitor token usage and costs
- Track agent conversation quality

### Development
- Use `.env.example` as a template
- Test locally before deploying
- Use feature flags for gradual rollouts
- Maintain separate dev/staging/prod environments

## Next Steps

1. **Customize the agent**: Modify `agent.py` to add your own instructions and tools
2. **Add more MCP tools**: Connect to additional knowledge sources
3. **Implement authentication**: Add user authentication for production
4. **Create a frontend**: Build a React/Vue/Angular app using CopilotKit
5. **Monitor and optimize**: Set up monitoring and improve based on usage

## Additional Resources

- [MCP Tools Documentation](https://modelcontextprotocol.io/)
- [Azure AI Services](https://azure.microsoft.com/en-us/products/ai-services)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CopilotKit Documentation](https://docs.copilotkit.ai/)
