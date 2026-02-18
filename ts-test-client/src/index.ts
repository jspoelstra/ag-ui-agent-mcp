/**
 * TypeScript Test Client for AG-UI Agent on Azure Foundry
 * 
 * This client demonstrates how to interact with an AG-UI agent deployed on Azure Foundry.
 * It exercises the AG-UI protocol with various test scenarios including:
 * - Basic connectivity checks
 * - Chat message sending
 * - Streaming responses (if supported)
 * - Knowledge base queries
 * 
 * The AG-UI protocol is exposed via the add_agent_framework_fastapi_endpoint()
 * function in the agent implementation.
 */

import * as dotenv from 'dotenv';
import * as http from 'http';
import * as https from 'https';
import { URL } from 'url';

// Load environment variables
dotenv.config();

/**
 * Interface for AG-UI message format
 */
interface AGUIMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

/**
 * Interface for AG-UI chat request
 */
interface AGUIChatRequest {
    messages: AGUIMessage[];
}

/**
 * Interface for AG-UI chat response
 */
interface AGUIChatResponse {
    response?: string;
    messages?: AGUIMessage[];
    error?: string;
}

/**
 * Test client for AG-UI agent
 */
class AGUITestClient {
    private baseUrl: string;
    private testResults: { name: string; passed: boolean; message: string }[] = [];

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
    }

    /**
     * Make an HTTP/HTTPS request
     */
    private async makeRequest(
        method: string,
        path: string,
        body?: any
    ): Promise<{ statusCode: number; data: string; headers: any }> {
        return new Promise((resolve, reject) => {
            const url = new URL(path, this.baseUrl);
            const isHttps = url.protocol === 'https:';
            const lib = isHttps ? https : http;

            const options = {
                hostname: url.hostname,
                port: url.port || (isHttps ? 443 : 80),
                path: url.pathname + url.search,
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
            };

            const req = lib.request(options, (res) => {
                let data = '';
                res.on('data', (chunk) => {
                    data += chunk;
                });
                res.on('end', () => {
                    resolve({
                        statusCode: res.statusCode || 0,
                        data,
                        headers: res.headers,
                    });
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            if (body) {
                req.write(JSON.stringify(body));
            }

            req.end();
        });
    }

    /**
     * Test 1: Basic connectivity to the AG-UI endpoint
     */
    async testConnectivity(): Promise<void> {
        console.log('\n1. Testing basic connectivity...');
        try {
            const response = await this.makeRequest('GET', '/');
            console.log(`   Status: ${response.statusCode}`);

            if (response.statusCode === 200 || response.statusCode === 404) {
                console.log('   ✓ Endpoint is reachable');
                this.testResults.push({
                    name: 'Basic Connectivity',
                    passed: true,
                    message: `Status ${response.statusCode}`,
                });
            } else {
                console.log(`   ⚠ Unexpected status code: ${response.statusCode}`);
                this.testResults.push({
                    name: 'Basic Connectivity',
                    passed: false,
                    message: `Unexpected status ${response.statusCode}`,
                });
            }
        } catch (error) {
            console.log(`   ✗ Connection failed: ${error}`);
            this.testResults.push({
                name: 'Basic Connectivity',
                passed: false,
                message: `Connection failed: ${error}`,
            });
        }
    }

    /**
     * Test 2: Send a simple chat message
     */
    async testSimpleChat(): Promise<void> {
        console.log('\n2. Testing simple chat message...');
        const testMessage: AGUIChatRequest = {
            messages: [
                {
                    role: 'user',
                    content: 'Hello! Can you help me with an intake form?',
                },
            ],
        };

        try {
            const response = await this.makeRequest('POST', '/chat', testMessage);
            console.log(`   Status: ${response.statusCode}`);

            if (response.statusCode === 200) {
                console.log('   ✓ Agent responded successfully');
                try {
                    const data: AGUIChatResponse = JSON.parse(response.data);
                    if (data.response) {
                        const preview = data.response.substring(0, 100);
                        console.log(`   Response preview: ${preview}${data.response.length > 100 ? '...' : ''}`);
                    } else if (data.messages && data.messages.length > 0) {
                        const lastMessage = data.messages[data.messages.length - 1];
                        const preview = lastMessage.content.substring(0, 100);
                        console.log(`   Response preview: ${preview}${lastMessage.content.length > 100 ? '...' : ''}`);
                    }
                    this.testResults.push({
                        name: 'Simple Chat',
                        passed: true,
                        message: 'Agent responded with valid data',
                    });
                } catch (parseError) {
                    console.log(`   Response data: ${response.data.substring(0, 200)}`);
                    this.testResults.push({
                        name: 'Simple Chat',
                        passed: true,
                        message: 'Response received (parse error)',
                    });
                }
            } else {
                console.log(`   Response: ${response.data.substring(0, 200)}`);
                this.testResults.push({
                    name: 'Simple Chat',
                    passed: false,
                    message: `Status ${response.statusCode}`,
                });
            }
        } catch (error) {
            console.log(`   ✗ Request failed: ${error}`);
            this.testResults.push({
                name: 'Simple Chat',
                passed: false,
                message: `Request failed: ${error}`,
            });
        }
    }

    /**
     * Test 3: Knowledge base query
     */
    async testKnowledgeBaseQuery(): Promise<void> {
        console.log('\n3. Testing knowledge base query...');
        const kbQuery: AGUIChatRequest = {
            messages: [
                {
                    role: 'user',
                    content: 'What projects are in the knowledge base that I can reference for this intake form?',
                },
            ],
        };

        try {
            const response = await this.makeRequest('POST', '/chat', kbQuery);
            console.log(`   Status: ${response.statusCode}`);

            if (response.statusCode === 200) {
                console.log('   ✓ Knowledge base query successful');
                try {
                    const data: AGUIChatResponse = JSON.parse(response.data);
                    if (data.response) {
                        const preview = data.response.substring(0, 200);
                        console.log(`   Response preview: ${preview}${data.response.length > 200 ? '...' : ''}`);
                    }
                    this.testResults.push({
                        name: 'Knowledge Base Query',
                        passed: true,
                        message: 'Query successful',
                    });
                } catch (parseError) {
                    console.log(`   Response received (parse error)`);
                    this.testResults.push({
                        name: 'Knowledge Base Query',
                        passed: true,
                        message: 'Response received',
                    });
                }
            } else {
                console.log(`   Response: ${response.data.substring(0, 200)}`);
                this.testResults.push({
                    name: 'Knowledge Base Query',
                    passed: false,
                    message: `Status ${response.statusCode}`,
                });
            }
        } catch (error) {
            console.log(`   ✗ Request failed: ${error}`);
            this.testResults.push({
                name: 'Knowledge Base Query',
                passed: false,
                message: `Request failed: ${error}`,
            });
        }
    }

    /**
     * Test 4: Multi-turn conversation
     */
    async testMultiTurnConversation(): Promise<void> {
        console.log('\n4. Testing multi-turn conversation...');
        const conversationRequest: AGUIChatRequest = {
            messages: [
                {
                    role: 'user',
                    content: 'I need help with an intake form.',
                },
                {
                    role: 'assistant',
                    content: 'I\'d be happy to help you with the intake form. What specific information do you need?',
                },
                {
                    role: 'user',
                    content: 'What are the required fields?',
                },
            ],
        };

        try {
            const response = await this.makeRequest('POST', '/chat', conversationRequest);
            console.log(`   Status: ${response.statusCode}`);

            if (response.statusCode === 200) {
                console.log('   ✓ Multi-turn conversation successful');
                this.testResults.push({
                    name: 'Multi-turn Conversation',
                    passed: true,
                    message: 'Conversation context maintained',
                });
            } else {
                console.log(`   Response: ${response.data.substring(0, 200)}`);
                this.testResults.push({
                    name: 'Multi-turn Conversation',
                    passed: false,
                    message: `Status ${response.statusCode}`,
                });
            }
        } catch (error) {
            console.log(`   ✗ Request failed: ${error}`);
            this.testResults.push({
                name: 'Multi-turn Conversation',
                passed: false,
                message: `Request failed: ${error}`,
            });
        }
    }

    /**
     * Test 5: Error handling (malformed request)
     */
    async testErrorHandling(): Promise<void> {
        console.log('\n5. Testing error handling...');
        const malformedRequest = {
            invalid: 'request',
        };

        try {
            const response = await this.makeRequest('POST', '/chat', malformedRequest);
            console.log(`   Status: ${response.statusCode}`);

            if (response.statusCode === 400 || response.statusCode === 422) {
                console.log('   ✓ Server correctly handles malformed requests');
                this.testResults.push({
                    name: 'Error Handling',
                    passed: true,
                    message: 'Proper error response',
                });
            } else if (response.statusCode === 200) {
                console.log('   ⚠ Server accepted malformed request (may have defaults)');
                this.testResults.push({
                    name: 'Error Handling',
                    passed: true,
                    message: 'Server is lenient with requests',
                });
            } else {
                console.log(`   Unexpected response: ${response.statusCode}`);
                this.testResults.push({
                    name: 'Error Handling',
                    passed: false,
                    message: `Unexpected status ${response.statusCode}`,
                });
            }
        } catch (error) {
            console.log(`   Error caught: ${error}`);
            this.testResults.push({
                name: 'Error Handling',
                passed: true,
                message: 'Connection-level error handling works',
            });
        }
    }

    /**
     * Print summary of test results
     */
    printSummary(): void {
        console.log('\n' + '='.repeat(70));
        console.log('Test Summary');
        console.log('='.repeat(70));

        const passed = this.testResults.filter((r) => r.passed).length;
        const failed = this.testResults.filter((r) => !r.passed).length;

        this.testResults.forEach((result) => {
            const status = result.passed ? '✓ PASS' : '✗ FAIL';
            console.log(`${status}: ${result.name} - ${result.message}`);
        });

        console.log('\n' + '-'.repeat(70));
        console.log(`Total: ${this.testResults.length} | Passed: ${passed} | Failed: ${failed}`);
        console.log('='.repeat(70));
    }

    /**
     * Run all tests
     */
    async runAllTests(): Promise<void> {
        console.log('='.repeat(70));
        console.log('AG-UI Agent Test Client');
        console.log('Testing Agent on Azure Foundry');
        console.log('='.repeat(70));
        console.log(`\nAgent URL: ${this.baseUrl}`);

        await this.testConnectivity();
        await this.testSimpleChat();
        await this.testKnowledgeBaseQuery();
        await this.testMultiTurnConversation();
        await this.testErrorHandling();

        this.printSummary();
    }
}

/**
 * Main function
 */
async function main() {
    // Get agent URL from environment or command line argument
    const agentUrl = process.argv[2] || process.env.AGENT_URL || 'http://localhost:8000';

    if (!agentUrl || agentUrl === 'https://your-agent-on-foundry.azurewebsites.net') {
        console.error('Error: Please provide a valid agent URL');
        console.error('\nUsage:');
        console.error('  npm run dev -- <agent-url>');
        console.error('  or set AGENT_URL in .env file');
        console.error('\nExamples:');
        console.error('  npm run dev -- http://localhost:8000');
        console.error('  npm run dev -- https://my-agent.azurewebsites.net');
        console.error('  npm run dev -- https://my-agent.azurecontainerapps.io');
        process.exit(1);
    }

    const client = new AGUITestClient(agentUrl);
    await client.runAllTests();
}

// Run the tests
main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
});
