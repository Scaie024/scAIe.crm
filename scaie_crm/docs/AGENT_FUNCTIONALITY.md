# SCAIE Agent Functionality Documentation

## Overview

The SCAIE system features two main agent implementations:

1. **Basic LLM Service** - A simple interface to the Qwen language model
2. **Omnipotent Agent** - An advanced agent with full CRM integration and action processing capabilities

## Omnipotent Agent

The Omnipotent Agent is the core intelligence of the SCAIE system. It provides advanced functionality beyond simple chat responses, including:

### Key Features

- **Contact Management**: Automatically creates and updates contact records
- **Interest Level Tracking**: Tracks and updates contact interest levels based on conversation content
- **Action Processing**: Determines and executes appropriate actions based on message content
- **Task Management**: Creates and manages follow-up tasks
- **Conversation Context**: Maintains conversation history and context
- **Multi-platform Support**: Works across web, WhatsApp, Telegram, and other platforms

### API Endpoints

#### Process Message
- **Endpoint**: `POST /api/omnipotent-agent/process-message`
- **Description**: Processes an incoming message and generates an appropriate response with actions
- **Request Body**:
  ```json
  {
    "message": "string",
    "platform": "string",
    "contact_info": {
      "name": "string (optional)",
      "phone": "string (optional)",
      "email": "string (optional)",
      "company": "string (optional)",
      "platform_user_id": "string (optional)"
    }
  }
  ```
- **Response**:
  ```json
  {
    "response": "string",
    "contact_id": "integer",
    "message_id": "integer",
    "actions": "array",
    "executed_actions": "array"
  }
  ```

#### Execute Pending Actions
- **Endpoint**: `POST /api/omnipotent-agent/execute-pending-actions/{conversation_id}`
- **Description**: Executes all pending actions for a conversation
- **Response**:
  ```json
  {
    "results": "array"
  }
  ```

### Agent Capabilities

#### Contact Management
The agent automatically manages contact information:
- Creates new contacts when they don't exist
- Updates existing contact information
- Tracks contact interest levels (NEW, LOW, MEDIUM, HIGH, CLIENT)

#### Action Processing
The agent can determine and process various actions:
- Sending materials (brochures, documents)
- Scheduling appointments
- Creating follow-up tasks
- Escalating to human agents

#### Conversation Context
The agent maintains context throughout conversations:
- Remembers previous messages in the conversation
- Tracks conversation state
- Uses context to provide more relevant responses

## Integration with Frontend

The frontend chat interface uses the Omnipotent Agent endpoint to provide a full-featured chat experience:
- Messages are sent to `/api/omnipotent-agent/process-message`
- Contact information is included with each message
- Responses include both the agent's reply and any actions to be taken

## Database Integration

The agent works with the following database models:
- **Contact**: Stores contact information and interest levels
- **Conversation**: Tracks conversation history
- **Message**: Stores individual messages
- **AgentAction**: Records actions determined by the agent
- **AgentTask**: Manages follow-up tasks

## Configuration

The agent can be configured through environment variables:
- `AGENT_NAME`: The name of the agent
- `AGENT_PERSONALITY`: Personality traits of the agent
- `AGENT_TONE`: Communication tone
- `AGENT_GOAL`: Primary goal of the agent

## Best Practices

1. **Use the Omnipotent Agent**: For full functionality, always use the omnipotent agent endpoint rather than the basic chat endpoint
2. **Provide Contact Information**: Always include contact information with messages for proper tracking
3. **Process Actions**: Implement action processing in your frontend to take advantage of agent capabilities
4. **Monitor Interest Levels**: Use the contact management features to track and respond to customer interest