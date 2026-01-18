"""SQLAlchemy database models for the Research Agent web UI."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class Session(Base):
    """Chat session/conversation."""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

    # Relationships
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    session_documents = relationship("SessionDocument", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(id={self.id}, title='{self.title}')>"


class Message(Base):
    """Chat message (user query or agent response)."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Research metadata (for assistant messages)
    sources = Column(JSON, nullable=True)  # List of source file paths
    documents_used = Column(Integer, nullable=True)
    relevance_score = Column(Float, nullable=True)
    iterations = Column(Integer, nullable=True)

    # Relationships
    session = relationship("Session", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', session_id={self.session_id})>"


class Document(Base):
    """Uploaded document metadata."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, unique=True, index=True)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False, unique=True)
    file_type = Column(String(50), nullable=False)  # pdf, txt, md
    file_size = Column(Integer, nullable=False)  # bytes
    chunks_count = Column(Integer, nullable=True)  # number of chunks ingested
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_ingested = Column(Boolean, default=False, nullable=False)
    ingestion_status = Column(String(50), default="pending", nullable=False)  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)

    # Relationships
    session_documents = relationship("SessionDocument", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', status='{self.ingestion_status}')>"


class SessionDocument(Base):
    """Many-to-many relationship between sessions and documents."""
    __tablename__ = "session_documents"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("Session", back_populates="session_documents")
    document = relationship("Document", back_populates="session_documents")

    def __repr__(self):
        return f"<SessionDocument(session_id={self.session_id}, document_id={self.document_id})>"
