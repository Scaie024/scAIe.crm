from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict

class AgentStats(BaseModel):
    total_contacts: int
    total_conversations: int
    total_messages: int
    total_actions: int

class ContactSummary(BaseModel):
    id: int
    name: str
    phone: str
    interest_level: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)

class OmnipotentAgentProcessRequest(BaseModel):
    message: str
    platform: str
    contact_info: Dict[str, Any]

class OmnipotentAgentProcessResponse(BaseModel):
    response: str
    contact_id: int
    message_id: int
    actions: List[Dict[str, Any]]
    executed_actions: List[Dict[str, Any]]

class OmnipotentAgentTaskCreate(BaseModel):
    contact_id: int
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[str] = None

class OmnipotentAgentTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    completed_at: Optional[str] = None

class OmnipotentAgentTask(BaseModel):
    id: int
    contact_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[str]
    created_at: str
    completed_at: Optional[str]