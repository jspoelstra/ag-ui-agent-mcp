// Azure AI Foundry Project deployment with hosted agent
// This template creates an AI Foundry project and deploys the hosted agent

@description('Name of the AI Project')
param projectName string

@description('Location for all resources')
param location string

@description('Name of the agent to deploy')
param agentName string

@description('Model to use for the agent')
param agentModel string

@description('MCP Server URL for knowledge base access')
param mcpServerUrl string

@description('Minimum number of instances for auto-scaling')
param minInstances int

@description('Maximum number of instances for auto-scaling')
param maxInstances int

@description('Resource tags')
param tags object

// AI Hub (required for AI Foundry Project)
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: 'aihub-${projectName}'
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: 'AI Hub for ${projectName}'
    friendlyName: 'AI Hub - ${projectName}'
    // AI Hub specific properties
    kind: 'Hub'
  }
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
}

// AI Foundry Project
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: projectName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: 'AI Foundry Project for AG-UI agent with MCP tools'
    friendlyName: projectName
    // Link to AI Hub
    hubResourceId: aiHub.id
    kind: 'Project'
  }
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
}

// Container Registry for hosting agent images
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'acr${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  sku: {
    name: 'Standard'
  }
  properties: {
    adminUserEnabled: true
  }
}

// Azure OpenAI Service for model hosting
resource openAiService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'openai-${projectName}'
  location: location
  tags: tags
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: 'openai-${uniqueString(resourceGroup().id)}'
    publicNetworkAccess: 'Enabled'
  }
}

// Deploy the model
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAiService
  name: agentModel
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: agentModel
      version: '1'
    }
  }
}

// Application Insights for monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${projectName}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-${projectName}'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Outputs
output projectEndpoint string = aiProject.properties.discoveryUrl
output projectName string = aiProject.name
output projectId string = aiProject.id
output agentEndpoint string = 'https://${aiProject.name}.${location}.inference.ai.azure.com/agents/${agentName}'
output containerRegistryName string = containerRegistry.name
output openAiEndpoint string = openAiService.properties.endpoint
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
