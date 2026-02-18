// Azure AI Foundry Project deployment with hosted agent
// This template creates an AI Foundry project and deploys the hosted agent
// Supports both creating new infrastructure and using existing Foundry projects

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

@description('Use existing AI Foundry project instead of creating new one')
param useExistingProject bool = false

@description('Existing AI Project resource ID (required if useExistingProject is true)')
param existingProjectId string = ''

// AI Hub (required for AI Foundry Project) - only created if not using existing project
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = if (!useExistingProject) {
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

// AI Foundry Project - created only if not using existing, referenced if using existing
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = if (!useExistingProject) {
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

// Reference to existing AI Project (if using existing)
// Azure Resource ID format: /subscriptions/{sub}/resourceGroups/{rg}/providers/{provider}/workspaces/{name}
// Index 8 in the split array is the workspace name
resource existingAiProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01' existing = if (useExistingProject) {
  name: useExistingProject ? split(existingProjectId, '/')[8] : 'placeholder'
  scope: resourceGroup()
}

// Determine which project to use for outputs
var activeProject = useExistingProject ? existingAiProject : aiProject

// Container Registry for hosting agent images - only created if not using existing project
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = if (!useExistingProject) {
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

// Azure OpenAI Service for model hosting - only created if not using existing project
resource openAiService 'Microsoft.CognitiveServices/accounts@2023-05-01' = if (!useExistingProject) {
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

// Deploy the model - only if creating new project
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = if (!useExistingProject) {
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

// Application Insights for monitoring - always created for the agent
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${projectName}-${agentName}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Log Analytics Workspace - always created for the agent
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-${projectName}-${agentName}'
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
output projectEndpoint string = activeProject.properties.discoveryUrl
output projectName string = activeProject.name
output projectId string = activeProject.id
output agentEndpoint string = 'https://${activeProject.name}.${location}.inference.ai.azure.com/agents/${agentName}'
output containerRegistryName string = useExistingProject ? 'using-existing' : containerRegistry.name
output openAiEndpoint string = useExistingProject ? 'using-existing' : openAiService.properties.endpoint
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
