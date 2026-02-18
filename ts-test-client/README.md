# TypeScript Test Client for AG-UI Agent on Azure Foundry

A simple TypeScript application that tests and exercises the AG-UI protocol for agents deployed on Azure Foundry (or any other endpoint).

## Overview

This test client demonstrates how to:
- Connect to an AG-UI agent endpoint deployed on Azure Foundry
- Send chat messages using the AG-UI protocol
- Handle responses from the agent
- Test various scenarios including knowledge base queries
- Validate multi-turn conversations
- Test error handling

## Features

The test client includes the following test scenarios:

1. **Basic Connectivity** - Verifies the agent endpoint is reachable
2. **Simple Chat** - Sends a basic message and receives a response
3. **Knowledge Base Query** - Tests MCP tool integration for knowledge retrieval
4. **Multi-turn Conversation** - Validates conversation context handling
5. **Error Handling** - Tests how the agent handles malformed requests

## Prerequisites

- Node.js 18.x or higher
- npm or yarn
- An AG-UI agent deployed on Azure Foundry (or accessible endpoint)

## Installation

```bash
# Navigate to the test client directory
cd ts-test-client

# Install dependencies
npm install
```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your agent URL:
   ```bash
   AGENT_URL=https://your-agent.azurewebsites.net
   ```

   **Example URLs:**
   - Local development: `http://localhost:8000`
   - Azure Container Apps: `https://your-app.azurecontainerapps.io`
   - Azure App Service: `https://your-app.azurewebsites.net`
   - Custom deployment: `https://your-custom-domain.com`

## Usage

### Option 1: Using environment variable from .env file

```bash
# Run in development mode (with ts-node)
npm run dev

# Or build and run
npm run build
npm start
```

### Option 2: Pass URL as command line argument

```bash
# Development mode
npm run dev -- http://localhost:8000
npm run dev -- https://my-agent.azurewebsites.net

# Production mode
npm run build
npm start -- https://my-agent.azurewebsites.net
```

### Option 3: Direct execution with ts-node

```bash
npx ts-node src/index.ts http://localhost:8000
```

## Expected Output

When you run the test client, you should see output similar to:

```
======================================================================
AG-UI Agent Test Client
Testing Agent on Azure Foundry
======================================================================

Agent URL: https://your-agent.azurewebsites.net

1. Testing basic connectivity...
   Status: 200
   ✓ Endpoint is reachable

2. Testing simple chat message...
   Status: 200
   ✓ Agent responded successfully
   Response preview: I'd be happy to help you with the intake form. What specific information...

3. Testing knowledge base query...
   Status: 200
   ✓ Knowledge base query successful
   Response preview: Based on the knowledge base, here are some projects you can reference...

4. Testing multi-turn conversation...
   Status: 200
   ✓ Multi-turn conversation successful

5. Testing error handling...
   Status: 422
   ✓ Server correctly handles malformed requests

======================================================================
Test Summary
======================================================================
✓ PASS: Basic Connectivity - Status 200
✓ PASS: Simple Chat - Agent responded with valid data
✓ PASS: Knowledge Base Query - Query successful
✓ PASS: Multi-turn Conversation - Conversation context maintained
✓ PASS: Error Handling - Proper error response

----------------------------------------------------------------------
Total: 5 | Passed: 5 | Failed: 0
======================================================================
```

## Testing Against Different Endpoints

### Testing Local Development

```bash
# Start your agent locally first
cd ..
python agent.py

# In another terminal, run the test client
cd ts-test-client
npm run dev -- http://localhost:8000
```

### Testing Azure Container Apps

```bash
# Get your Container App URL
az containerapp show \
  --name ag-ui-agent-mcp \
  --resource-group rg-ag-ui-agent \
  --query properties.configuration.ingress.fqdn \
  --output tsv

# Test against it
npm run dev -- https://<your-app>.azurecontainerapps.io
```

### Testing Azure App Service

```bash
# Get your App Service URL
az webapp show \
  --name your-app-name \
  --resource-group rg-ag-ui-agent \
  --query defaultHostName \
  --output tsv

# Test against it
npm run dev -- https://<your-app>.azurewebsites.net
```

## Understanding the AG-UI Protocol

The AG-UI protocol is a standard protocol for agent communication. This test client demonstrates the basic request/response format:

### Request Format

```typescript
{
  "messages": [
    {
      "role": "user",
      "content": "Your message here"
    }
  ]
}
```

### Response Format

The response can vary, but typically includes:

```typescript
{
  "response": "Agent's response text",
  // or
  "messages": [
    {
      "role": "assistant",
      "content": "Agent's response text"
    }
  ]
}
```

## Project Structure

```
ts-test-client/
├── src/
│   └── index.ts          # Main test client implementation
├── dist/                 # Compiled JavaScript (after build)
├── package.json          # Node.js dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── .env.example          # Example environment configuration
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Development

### Building the Project

```bash
npm run build
```

This compiles TypeScript to JavaScript in the `dist/` directory.

### Running TypeScript Directly

```bash
npm run dev
```

This uses `ts-node` to run TypeScript without compilation.

### Adding New Tests

To add a new test scenario, modify `src/index.ts`:

1. Add a new test method to the `AGUITestClient` class
2. Call it from the `runAllTests()` method
3. Update the test summary

Example:

```typescript
async testCustomScenario(): Promise<void> {
    console.log('\n6. Testing custom scenario...');
    // Your test implementation
}

async runAllTests(): Promise<void> {
    // ... existing tests
    await this.testCustomScenario();
    // ...
}
```

## Troubleshooting

### Connection Errors

If you see connection errors:

1. Verify the agent URL is correct
2. Check if the agent is running (for local testing)
3. Verify network connectivity to Azure (for Foundry deployments)
4. Check firewall rules and security groups

### Authentication Errors

If the agent requires authentication:

1. Update the `makeRequest` method to include authentication headers
2. Add bearer tokens or API keys as needed

Example:

```typescript
headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.AUTH_TOKEN}`,
},
```

### SSL Certificate Issues

For development/testing with self-signed certificates:

```bash
# Run with NODE_TLS_REJECT_UNAUTHORIZED=0 (development only!)
NODE_TLS_REJECT_UNAUTHORIZED=0 npm run dev -- https://localhost:8000
```

**Note:** Never disable SSL validation in production.

## Integration with CI/CD

You can use this test client in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Install test client dependencies
  run: |
    cd ts-test-client
    npm install

- name: Run AG-UI tests
  run: |
    cd ts-test-client
    npm run build
    npm start -- ${{ secrets.AGENT_URL }}
```

## Related Documentation

- [Parent Project README](../README.md) - Main agent implementation
- [AG-UI and Foundry Explained](../AG_UI_AND_FOUNDRY_EXPLAINED.md) - Detailed protocol explanation
- [Usage Guide](../USAGE.md) - How to deploy and run the agent
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) - Official documentation
- [AG-UI Protocol Specification](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/) - Protocol details

## License

MIT

## Contributing

Contributions are welcome! Feel free to:
- Add new test scenarios
- Improve error handling
- Add authentication support
- Enhance reporting
