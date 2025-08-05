"""
Module to define relationships between models to avoid circular imports.
This file should be imported after all models are defined.
"""

from sqlalchemy.orm import relationship

# Import all models
from .contact import Contact
from .conversation import Conversation, Message
from .agent_action import AgentAction, AgentTask

# Define relationships for Contact
Contact.conversations = relationship("Conversation", back_populates="contact", cascade="all, delete-orphan")
Contact.messages = relationship("Message", back_populates="contact")
Contact.tasks = relationship("AgentTask", back_populates="contact")

# Define relationships for Conversation
Conversation.messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
Conversation.contact = relationship("Contact", back_populates="conversations")
Conversation.actions = relationship("AgentAction", back_populates="conversation", cascade="all, delete-orphan")

# Define relationships for Message
Message.conversation = relationship("Conversation", back_populates="messages")
Message.contact = relationship("Contact", back_populates="messages")

# Define relationships for AgentAction
AgentAction.conversation = relationship("Conversation", back_populates="actions")

# Define relationships for AgentTask
AgentTask.contact = relationship("Contact", back_populates="tasks")