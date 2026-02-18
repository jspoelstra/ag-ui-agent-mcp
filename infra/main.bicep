// Main infrastructure deployment for Azure AI Foundry hosted agent
// This template provisions the necessary Azure resources for hosting the agent on Foundry

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

@description('Resource group name')
param resourceGroupName string = 'rg-${aiProjectName}'

@description('Tags to apply to all resources')
param tags object = {
  'azd-env-name': aiProjectName
  'deployment-type': 'foundry-hosted-agent'
  'framework': 'microsoft-agent-framework'
  'protocol': 'ag-ui'
}

// Resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

// Deploy the AI Foundry project and agent resources
module foundryProject './foundry-project.bicep' = {
  name: 'foundry-project-deployment'
  scope: rg
  params: {
    projectName: aiProjectName
    location: location
    agentName: agentName
    agentModel: agentModel
    mcpServerUrl: mcpServerUrl
    minInstances: minInstances
    maxInstances: maxInstances
    tags: tags
  }
}

// Outputs
output AZURE_AI_PROJECT_ENDPOINT string = foundryProject.outputs.projectEndpoint
output AZURE_AI_PROJECT_NAME string = foundryProject.outputs.projectName
output AGENT_ENDPOINT string = foundryProject.outputs.agentEndpoint
output RESOURCE_GROUP_NAME string = rg.name
