"""CRUD operations for database models."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.database.models import Session as SessionModel, Message, Document, SessionDocument


# ==================== Session CRUD ====================

def create_session(db: Session, title: str = "New Research Session") -> SessionModel:
    """Create a new chat session."""
    session = SessionModel(title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int) -> Optional[SessionModel]:
    """Get a session by ID."""
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()


def get_sessions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    include_archived: bool = False
) -> List[SessionModel]:
    """Get all sessions."""
    query = db.query(SessionModel)
    if not include_archived:
        query = query.filter(SessionModel.is_archived == False)
    return query.order_by(desc(SessionModel.updated_at)).offset(skip).limit(limit).all()


def update_session(
    db: Session,
    session_id: int,
    title: Optional[str] = None,
    is_archived: Optional[bool] = None
) -> Optional[SessionModel]:
    """Update a session."""
    session = get_session(db, session_id)
    if not session:
        return None

    if title is not None:
        session.title = title
    if is_archived is not None:
        session.is_archived = is_archived

    session.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, session_id: int) -> bool:
    """Delete a session and all its messages."""
    session = get_session(db, session_id)
    if not session:
        return False

    db.delete(session)
    db.commit()
    return True


# ==================== Message CRUD ====================

def create_message(
    db: Session,
    session_id: int,
    role: str,
    content: str,
    sources: Optional[List[str]] = None,
    documents_used: Optional[int] = None,
    relevance_score: Optional[float] = None,
    iterations: Optional[int] = None
) -> Message:
    """Create a new message."""
    message = Message(
        session_id=session_id,
        role=role,
        content=content,
        sources=sources,
        documents_used=documents_used,
        relevance_score=relevance_score,
        iterations=iterations
    )
    db.add(message)

    # Update session's updated_at
    session = get_session(db, session_id)
    if session:
        session.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, session_id: int) -> List[Message]:
    """Get all messages for a session."""
    return db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()


def get_message(db: Session, message_id: int) -> Optional[Message]:
    """Get a message by ID."""
    return db.query(Message).filter(Message.id == message_id).first()


# ==================== Document CRUD ====================

def create_document(
    db: Session,
    filename: str,
    original_filename: str,
    file_path: str,
    file_type: str,
    file_size: int,
    ingestion_status: str = "pending"
) -> Document:
    """Create a new document record."""
    document = Document(
        filename=filename,
        original_filename=original_filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        ingestion_status=ingestion_status
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document(db: Session, document_id: int) -> Optional[Document]:
    """Get a document by ID."""
    return db.query(Document).filter(Document.id == document_id).first()


def get_documents(db: Session, skip: int = 0, limit: int = 100) -> List[Document]:
    """Get all documents."""
    return db.query(Document).order_by(desc(Document.uploaded_at)).offset(skip).limit(limit).all()


def update_document(
    db: Session,
    document_id: int,
    is_ingested: Optional[bool] = None,
    ingestion_status: Optional[str] = None,
    chunks_count: Optional[int] = None,
    error_message: Optional[str] = None
) -> Optional[Document]:
    """Update document status."""
    document = get_document(db, document_id)
    if not document:
        return None

    if is_ingested is not None:
        document.is_ingested = is_ingested
    if ingestion_status is not None:
        document.ingestion_status = ingestion_status
    if chunks_count is not None:
        document.chunks_count = chunks_count
    if error_message is not None:
        document.error_message = error_message

    db.commit()
    db.refresh(document)
    return document


def delete_document(db: Session, document_id: int) -> bool:
    """Delete a document."""
    document = get_document(db, document_id)
    if not document:
        return False

    db.delete(document)
    db.commit()
    return True


def get_document_stats(db: Session) -> dict:
    """Get document statistics."""
    total_documents = db.query(func.count(Document.id)).scalar()
    total_size = db.query(func.sum(Document.file_size)).scalar() or 0
    total_chunks = db.query(func.sum(Document.chunks_count)).filter(Document.chunks_count.isnot(None)).scalar() or 0

    # Count by type
    by_type = {}
    type_counts = db.query(Document.file_type, func.count(Document.id)).group_by(Document.file_type).all()
    for file_type, count in type_counts:
        by_type[file_type] = count

    return {
        "total_documents": total_documents,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "total_chunks": total_chunks,
        "by_type": by_type
    }


# ==================== SessionDocument CRUD ====================

def add_document_to_session(db: Session, session_id: int, document_id: int) -> SessionDocument:
    """Link a document to a session."""
    session_doc = SessionDocument(session_id=session_id, document_id=document_id)
    db.add(session_doc)
    db.commit()
    db.refresh(session_doc)
    return session_doc


def get_session_documents(db: Session, session_id: int) -> List[Document]:
    """Get all documents linked to a session."""
    return (
        db.query(Document)
        .join(SessionDocument)
        .filter(SessionDocument.session_id == session_id)
        .all()
    )
