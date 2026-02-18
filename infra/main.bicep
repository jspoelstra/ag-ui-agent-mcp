// Main infrastructure deployment for Azure AI Foundry hosted agent
// This template provisions the necessary Azure resources for hosting the agent on Foundry
// Supports both creating new infrastructure and reusing existing Foundry projects

targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the AI Project')
param aiProjectName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Name of the agent to deploy')
param agentName string = 'IntakeFormAssistant'

@description('Model to use for the agent')
param agentModel string = 'gpt-5-mini'

@description('MCP Server URL for knowledge base access')
param mcpServerUrl string

@description('Minimum number of instances for auto-scaling')
param minInstances int = 1

@description('Maximum number of instances for auto-scaling')
param maxInstances int = 10

@description('Resource group name (for new deployments) or existing resource group name')
param resourceGroupName string = 'rg-${aiProjectName}'

@description('Use existing AI Foundry project instead of creating new one')
param useExistingProject bool = false

@description('Existing AI Project resource ID (required if useExistingProject is true)')
param existingProjectId string = ''

@description('Existing resource group name (required if useExistingProject is true)')
param existingResourceGroupName string = ''

@description('Tags to apply to all resources')
param tags object = {
  'azd-env-name': aiProjectName
  'deployment-type': 'foundry-hosted-agent'
  'framework': 'microsoft-agent-framework'
  'protocol': 'ag-ui'
}

// Determine which resource group to use
var targetResourceGroupName = useExistingProject ? existingResourceGroupName : resourceGroupName

// Resource group (only created if not using existing project)
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = if (!useExistingProject) {
  name: resourceGroupName
  location: location
  tags: tags
}

// Reference to existing resource group (if using existing project)
resource existingRg 'Microsoft.Resources/resourceGroups@2021-04-01' existing = if (useExistingProject) {
  name: existingResourceGroupName
}

// Deploy the AI Foundry project and agent resources
module foundryProject './foundry-project.bicep' = {
  name: 'foundry-project-deployment'
  scope: useExistingProject ? existingRg : rg
  params: {
    projectName: aiProjectName
    location: location
    agentName: agentName
    agentModel: agentModel
    mcpServerUrl: mcpServerUrl
    minInstances: minInstances
    maxInstances: maxInstances
    tags: tags
    useExistingProject: useExistingProject
    existingProjectId: existingProjectId
  }
}

// Outputs
output AZURE_AI_PROJECT_ENDPOINT string = foundryProject.outputs.projectEndpoint
output AZURE_AI_PROJECT_NAME string = foundryProject.outputs.projectName
output AGENT_ENDPOINT string = foundryProject.outputs.agentEndpoint
output RESOURCE_GROUP_NAME string = targetResourceGroupName
output DEPLOYMENT_MODE string = useExistingProject ? 'existing-project' : 'new-project'
