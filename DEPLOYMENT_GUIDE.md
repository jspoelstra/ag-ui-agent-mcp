# Deployment Guide: Foundry v2 Hosted Agent

This guide walks you through deploying the agent as a fully managed service on Azure AI Foundry using the v2 hosted agent capability.

## Overview

With Foundry v2 hosted agents, your agent runs on Foundry's managed infrastructure instead of locally or in containers you manage. Benefits include:

- ✅ **Fully Managed**: Foundry handles all infrastructure, scaling, and monitoring
- ✅ **Simple Deployment**: One command (`azd up`) deploys everything
- ✅ **Auto-Scaling**: Automatically scales from 1-10 instances based on demand
- ✅ **Enterprise-Ready**: Built-in security, compliance, and governance
- ✅ **Cost-Effective**: Pay only for what you use
- ✅ **Integrated Monitoring**: Application Insights and logging included

## Prerequisites

### Required Tools

1. **Azure Developer CLI (azd)** - Version 1.23.0 or later
   ```bash
   # macOS/Linux
   curl -fsSL https://aka.ms/install-azd.sh | bash
   
   # Windows (PowerShell)
   winget install microsoft.azd
   
   # Verify installation
   azd version
   ```

2. **Azure CLI** - For authentication
   ```bash
   # Install if needed
   # macOS: brew install azure-cli
   # Windows: winget install microsoft.azurecli
   # Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   
   # Login to Azure
   az login
   ```

3. **Docker Desktop** - For building container images
   - Download from https://www.docker.com/products/docker-desktop/

### Azure Requirements

- **Azure Subscription**: Active Azure subscription with permissions to create resources
- **AI Foundry Access**: Access to Azure AI Foundry (formerly Azure AI Studio)
- **Resource Quota**: Ensure you have quota for:
  - AI Hub/Project
  - Container Registry
  - Azure OpenAI Service
  - Application Insights

## Step-by-Step Deployment

### 1. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/jspoelstra/ag-ui-agent-mcp.git
cd ag-ui-agent-mcp

# Create environment file
cp .env.example .env

# Edit .env with your configuration
# Required variables:
# - AZURE_AI_PROJECT_NAME=<your-project-name>
# - AZURE_LOCATION=<azure-region>  # e.g., eastus2
# - AGENT_MODEL=gpt-5-mini
# - MCP_SERVER_URL=<your-mcp-server-url>
```

### 2. Authenticate to Azure

```bash
# Login to Azure
az login

# Set your default subscription (if you have multiple)
az account set --subscription <subscription-id>

# Verify authentication
az account show
```

### 3. Initialize Deployment

```bash
# Initialize azd for this project
azd init

# Follow the prompts:
# - Environment name: Choose a name for this deployment (e.g., "dev", "prod")
# - Subscription: Select your Azure subscription
# - Location: Select Azure region (e.g., "eastus2")
```

### 4. Deploy to Foundry

```bash
# Deploy everything with a single command
azd up

# This will:
# 1. Provision Azure AI Foundry project
# 2. Create Azure Container Registry
# 3. Deploy Azure OpenAI Service
# 4. Set up Application Insights
# 5. Build and push Docker image
# 6. Deploy agent as hosted service
# 7. Configure auto-scaling
# 8. Expose AG-UI endpoint
```

### 5. Verify Deployment

```bash
# Check agent status
azd ai agent show

# View deployment details
azd env get-values

# View logs
azd monitor --logs

# Get the agent endpoint
azd env get-values | grep AGENT_ENDPOINT
```

## Post-Deployment

### Access Your Agent

The agent will be available at the Foundry-provided endpoint:

```
https://[project-name].[region].inference.ai.azure.com/agents/IntakeFormAssistant
```

### Test the AG-UI Endpoint

```bash
# Get authentication token
TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)

# Test the endpoint
curl -X POST https://[foundry-endpoint]/agents/IntakeFormAssistant/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "messages": [
      {"role": "user", "content": "Help me with an intake form"}
    ]
  }'
```

### Frontend Integration

Connect your frontend application to the AG-UI endpoint:

```typescript
// Example with CopilotKit
import { CopilotKit } from "@copilotkit/react-core";

<CopilotKit 
  runtimeUrl="https://[foundry-endpoint]/agents/IntakeFormAssistant"
  headers={{
    Authorization: `Bearer ${token}`
  }}
>
  {/* Your app components */}
</CopilotKit>
```

## Managing Your Deployment

### Update Agent

After making code changes:

```bash
# Deploy updates
azd deploy

# Or deploy everything (if infrastructure changed)
azd up
```

### View Logs and Monitoring

```bash
# View real-time logs
azd monitor --logs

# Open Azure Portal for detailed monitoring
azd monitor

# View Application Insights in browser
az portal
# Navigate to: Resource Group > Application Insights
```

### Scale Configuration

To adjust scaling limits, edit `agent.yaml`:

```yaml
deployment:
  scaling:
    min_instances: 2  # Increase minimum instances
    max_instances: 20  # Increase maximum instances
```

Then redeploy:

```bash
azd deploy
```

### Clean Up Resources

To delete all deployed resources:

```bash
# Delete the deployment
azd down

# Confirm deletion when prompted
```

**Warning**: This will delete all resources including the AI Project, Container Registry, and Application Insights.

## Troubleshooting

### Common Issues

#### 1. Authentication Errors

```bash
# Re-authenticate to Azure
az login

# Clear cached credentials
azd auth login
```

#### 2. Deployment Failures

```bash
# View detailed error messages
azd deploy --debug

# Check Azure portal for resource provisioning status
az portal
```

#### 3. Quota Exceeded

If deployment fails due to quota:

1. Go to Azure Portal
2. Navigate to Subscriptions > Usage + quotas
3. Request quota increase for required resources
4. Wait for approval and retry deployment

#### 4. Docker Build Errors

Ensure Docker Desktop is running:

```bash
# Check Docker status
docker info

# Restart Docker Desktop if needed
```

### Getting Help

- Check deployment logs: `azd monitor --logs`
- View Azure Portal: `az portal`
- Review Bicep templates in `infra/` directory
- Consult [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)

## Advanced Configuration

### Custom Infrastructure

Modify the Bicep templates in `infra/` directory:

- `main.bicep` - Main deployment orchestration
- `foundry-project.bicep` - AI Foundry project resources

### Environment Variables

Set additional environment variables in `azure.yaml`:

```yaml
services:
  agent:
    env:
      CUSTOM_VAR:
        value: custom-value
```

### Multiple Environments

Deploy to multiple environments (dev, staging, prod):

```bash
# Create dev environment
azd init -e dev
azd up

# Create prod environment
azd init -e prod
azd up

# Switch between environments
azd env select dev
azd deploy
```

## Cost Optimization

- **Auto-Scaling**: Configured to scale down to 1 instance when idle
- **Development**: Use cheaper regions during development
- **Monitoring**: Review cost analysis in Azure Portal regularly
- **Cleanup**: Delete unused deployments with `azd down`

## Security Best Practices

- **Managed Identity**: Used for authentication between services
- **Private Endpoints**: Consider adding for production deployments
- **Key Vault**: Store secrets in Azure Key Vault
- **Network Security**: Configure virtual networks in production
- **RBAC**: Apply least-privilege access control

## Next Steps

1. **Customize Agent**: Modify `agent.yaml` to customize behavior
2. **Add Tools**: Add more MCP tools in the agent configuration
3. **Monitor Performance**: Set up alerts in Application Insights
4. **Scale for Production**: Adjust scaling limits based on load
5. **Integrate Frontend**: Connect your application to the AG-UI endpoint

## Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure Developer CLI Documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Hosted Agents Guide](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)
- [AG-UI Protocol Specification](https://learn.microsoft.com/agent-framework/integrations/ag-ui/)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/)
