# AG-UI Support and Azure Foundry Deployment - Explained

This document addresses key questions about this implementation:

1. **Why does the code use `add_agent_framework_fastapi_endpoint` instead of direct AG-UI support?**
2. **How is the agent deployed on Microsoft Foundry on Azure?**
3. **What is the difference between Foundry v2 hosted agents and self-hosted deployment?**

## Important: Foundry v2 Hosted Agent Deployment

**This repository has been updated to use Foundry v2 hosted agent deployment.**

### What Changed?

**BEFORE (Legacy Self-Hosted):**
- Agent runs locally via `python agent.py`
- Or containerized and deployed to Azure Container Apps/App Service
- You manage the infrastructure, scaling, and monitoring
- AzureAIProjectAgentProvider connects to Foundry for models/tools only

**NOW (Foundry v2 Hosted):**
- Agent is deployed directly to Foundry's managed infrastructure
- Use `azd up` to deploy everything
- Foundry handles infrastructure, scaling, monitoring, and lifecycle
- No need to run locally or manage containers yourself

### How to Deploy as Hosted Agent

```bash
# 1. Initialize deployment (first time only)
azd init

# 2. Deploy to Foundry
azd up

# 3. View agent status
azd ai agent show
```

See the deployment sections below for details.

## 1. AG-UI Support - Why `add_agent_framework_fastapi_endpoint`?

### Short Answer
**The code DOES have AG-UI support!** The function `add_agent_framework_fastapi_endpoint` from the `agent-framework-ag-ui` package **IS** how you expose AG-UI protocol endpoints in the Microsoft Agent Framework.

### Detailed Explanation

The confusion might arise from thinking that `agent-framework-ag-ui` provides a different way to expose AG-UI. In reality:

#### The AG-UI Integration Flow:

```
agent-framework-ag-ui package
    ↓
Provides: add_agent_framework_fastapi_endpoint() function
    ↓
This function takes an Agent + FastAPI app
    ↓
Returns: FastAPI app with AG-UI protocol endpoints exposed
```

#### Code Breakdown (from agent.py):

```python
# Line 18: Import from the AG-UI package
from agent_framework.ag_ui import add_agent_framework_fastapi_endpoint

# Line 79: Use the function to expose AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")
```

**What this does:**
- Takes your MAF (Microsoft Agent Framework) agent
- Adds AG-UI protocol endpoints to the FastAPI app
- Enables frontend frameworks (like CopilotKit) to communicate with your agent
- Supports streaming, tool execution, and rich UI components

#### Why This Approach?

The Microsoft Agent Framework uses a layered architecture:

```
┌──────────────────────────────────────────────────┐
│  Frontend (CopilotKit, Custom UI)                │
│  Uses AG-UI Protocol                             │
└─────────────────────┬────────────────────────────┘
                      │ HTTP/WebSocket
                      │ AG-UI Protocol Messages
                      ↓
┌──────────────────────────────────────────────────┐
│  FastAPI Application                             │
│  With AG-UI endpoints added via                  │
│  add_agent_framework_fastapi_endpoint()          │
└─────────────────────┬────────────────────────────┘
                      │
                      ↓
┌──────────────────────────────────────────────────┐
│  Microsoft Agent Framework (MAF)                 │
│  Your Agent with tools, instructions, provider   │
└─────────────────────┬────────────────────────────┘
                      │
                      ↓
┌──────────────────────────────────────────────────┐
│  Azure AI / MCP Tools / External Services        │
└──────────────────────────────────────────────────┘
```

**Benefits of this approach:**
1. **Flexibility**: You control the FastAPI app and can add custom endpoints
2. **Standard Protocol**: AG-UI is an open protocol, not tied to one framework
3. **Composability**: You can add other middleware, authentication, etc.
4. **Production Ready**: FastAPI is battle-tested for production deployments

#### What AG-UI Provides

When you call `add_agent_framework_fastapi_endpoint(app, agent, "/")`, it adds these capabilities:

✅ **Chat Endpoint**: `/chat` for conversation messages
✅ **Streaming**: Server-sent events for real-time responses  
✅ **Tool Execution**: Transparent tool calling (MCP, functions, etc.)
✅ **State Management**: Conversation history and context
✅ **Error Handling**: Standardized error responses
✅ **Rich Components**: Support for UI components in responses

#### Verification

You can verify AG-UI support is working by:

```bash
# 1. Start the agent
python agent.py

# 2. Test the AG-UI endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

The response will be in AG-UI protocol format, compatible with CopilotKit and other AG-UI clients.

---

## 2. Azure Foundry Deployment - Hosted vs Self-Hosted

### Short Answer
This repository supports **two deployment modes**:

1. **Foundry v2 Hosted Agent (Recommended)**: Agent runs on Foundry's managed infrastructure
2. **Self-Hosted with Foundry Connection (Legacy)**: Agent runs locally/in containers but connects to Foundry

### Detailed Explanation

#### Foundry v2 Hosted Agent Deployment (Recommended)

With Foundry v2, you can deploy agents directly to Foundry's managed infrastructure:

**How It Works:**
```bash
# Deploy using Azure Developer CLI
azd up
```

**What happens:**
1. **Infrastructure Provisioning**: Bicep templates create Azure AI Foundry project
2. **Container Build**: Your agent is built as a Docker image
3. **Hosted Deployment**: Foundry deploys and manages your agent
4. **Auto-Scaling**: Foundry handles scaling based on demand
5. **Monitoring**: Integrated Application Insights and logging
6. **AG-UI Endpoint**: Automatically exposed and managed

**Files for Hosted Deployment:**
- `agent.yaml` - Agent definition and configuration
- `azure.yaml` - azd deployment configuration
- `infra/` - Bicep templates for Azure resources
- `Dockerfile` - Container image definition

**Benefits:**
✅ **Fully Managed**: Foundry handles infrastructure, scaling, updates
✅ **Enterprise-Ready**: Built-in security, compliance, governance
✅ **Cost-Effective**: Pay only for what you use, auto-scaling
✅ **Integrated**: Seamless Azure ecosystem integration
✅ **Simple Deployment**: One command (`azd up`) to deploy
✅ **No Infrastructure Management**: Focus on agent logic, not ops

**Deployment Architecture:**
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

#### Self-Hosted with Foundry Connection (Legacy)

The legacy approach where you manage the infrastructure but connect to Foundry:

**How It Works:**
```python
# In agent.py
async with AzureAIProjectAgentProvider() as provider:
    agent = await provider.create_agent(...)

# Run locally
python agent.py

# Or containerize and deploy to Azure Container Apps
docker build -t agent .
az containerapp create ...
```

**What happens:**
1. **Agent Runs Locally**: FastAPI server runs on your machine/container
2. **Connects to Foundry**: Uses AzureAIProjectAgentProvider for models
3. **You Manage Infrastructure**: You handle scaling, monitoring, deployment
4. **AG-UI Endpoint**: Exposed via FastAPI on your infrastructure

**When to Use:**
- Development and testing
- Custom infrastructure requirements
- Specific networking constraints
- Gradual migration to hosted agents

**Architecture:**
```
┌──────────────────────────────────┐
│  Your Infrastructure             │
│  ├─ Container/VM (your agent)    │
│  ├─ FastAPI (AG-UI endpoint)     │
│  └─ You manage scaling/monitoring│
└─────────────┬────────────────────┘
              │ AZURE_AI_PROJECT_CONNECTION_STRING
              ↓
┌──────────────────────────────────┐
│  Azure AI Project (Foundry)      │
│  ├─ Models (GPT-5-mini, etc.)    │
│  ├─ MCP Tools                    │
│  └─ Enterprise Security          │
└──────────────────────────────────┘
```

#### Code Breakdown (Self-Hosted agent.py):

```python
# Line 20: Import the Azure Foundry provider (for self-hosted mode)
from agent_framework.azure import AzureAIProjectAgentProvider

# Lines 48-58: Create agent using Foundry provider (connects to Foundry for models)
async with AzureAIProjectAgentProvider() as provider:
    agent = await provider.create_agent(
        name="IntakeFormAssistant",
        model=os.getenv("AGENT_MODEL", "gpt-5-mini"),
        instructions="""...""",
        tools=[mcp_kb_tool],
    )
```

**Note**: For hosted deployment, the agent.yaml file defines the agent configuration instead.

#### What `AzureAIProjectAgentProvider` Does (Self-Hosted Mode):

1. **Connects to Azure AI Project (Foundry)**
   - Uses `AZURE_AI_PROJECT_CONNECTION_STRING` from environment
   - Authenticates via `DefaultAzureCredential`
   - Establishes connection to your Foundry project

2. **Provisions Agent Resources**
   - Configures the specified model (gpt-5-mini, gpt-4, etc.)
   - Sets up the agent's tools and capabilities
   - Links to project resources (MCP connections, knowledge bases, etc.)

3. **Manages Agent Lifecycle**
   - Handles authentication and authorization
   - Manages model deployments
   - Coordinates with Azure services
   - Provides monitoring and logging integration

---

## 3. Comparison: Hosted vs Self-Hosted

| Feature | Foundry v2 Hosted | Self-Hosted with Foundry |
|---------|-------------------|--------------------------|
| **Infrastructure** | Managed by Foundry | You manage containers/VMs |
| **Deployment** | `azd up` | `python agent.py` or Docker |
| **Scaling** | Auto-scaling by Foundry | You configure scaling |
| **Monitoring** | Built-in Application Insights | You set up monitoring |
| **Cost** | Pay-per-use, auto-scale | Always-on or manual scaling |
| **Maintenance** | Foundry updates automatically | You apply updates |
| **Security** | Enterprise-grade built-in | You configure security |
| **AG-UI Endpoint** | Auto-exposed by Foundry | You expose via FastAPI |
| **Best For** | Production, enterprise | Development, custom needs |

---

## 4. Migration Path

### From Self-Hosted to Hosted Agent

If you have an existing self-hosted agent, here's how to migrate:

1. **Create agent.yaml** - Define your agent configuration
2. **Create azure.yaml** - Set up azd deployment
3. **Create infra/** - Add Bicep templates
4. **Deploy**: Run `azd up`
5. **Update clients** - Point to new Foundry endpoint
6. **Decommission old infrastructure** - Remove self-hosted resources

The agent logic remains the same; only the deployment method changes.

---
---

## 5. Summary

### AG-UI Support ✅
**Yes, this code has full AG-UI support** via the `agent-framework-ag-ui` package. The `add_agent_framework_fastapi_endpoint()` function is the official way to expose AG-UI endpoints.

### Azure Foundry Deployment ✅  
**This repository now supports Foundry v2 hosted agent deployment**. Deploy using `azd up` to have your agent fully managed by Azure AI Foundry.

### Deployment Options

**Option 1: Foundry v2 Hosted (Recommended for Production)**
```bash
azd up  # Deploy to Foundry's managed infrastructure
```
- Agent runs on Foundry's managed infrastructure
- Fully managed scaling, monitoring, updates
- Enterprise-grade security and compliance
- Simple one-command deployment

**Option 2: Self-Hosted (Development/Custom Needs)**
```bash
python agent.py  # Run locally with Foundry connection
```
- Agent runs on your infrastructure
- Connects to Foundry for models and tools
- You manage deployment and scaling
- Good for development and testing

### The Complete Picture (Hosted Agent)

```
1. Define agent in agent.yaml
   ↓
2. Configure deployment in azure.yaml
   ↓
3. Run: azd up
   ↓
4. Foundry provisions and deploys agent
   ↓
5. AG-UI endpoint automatically exposed
   ↓
6. Frontend connects to Foundry endpoint
```

**Result**: You have an agent that:
- ✅ Runs on Foundry's managed infrastructure
- ✅ Exposes AG-UI protocol endpoints  
- ✅ Connects to MCP tools
- ✅ Auto-scales based on demand
- ✅ Includes enterprise security and monitoring

---

## Further Reading

- **Microsoft Agent Framework**: https://learn.microsoft.com/agent-framework/
- **AG-UI Protocol**: https://learn.microsoft.com/agent-framework/integrations/ag-ui/
- **Azure AI Foundry**: https://learn.microsoft.com/azure/ai-studio/
- **Hosted Agents**: https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents
- **Azure Developer CLI**: https://learn.microsoft.com/azure/developer/azure-developer-cli/
- **MCP Tools**: https://modelcontextprotocol.io/
