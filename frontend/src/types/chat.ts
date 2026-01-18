export interface Message {
  id: number
  session_id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
  sources?: string[]
  documents_used?: number
  relevance_score?: number
  iterations?: number
}

export interface Session {
  id: number
  title: string
  created_at: string
  updated_at: string
  is_archived: boolean
  message_count: number
}

export interface SessionDetail extends Omit<Session, 'message_count'> {
  messages: Message[]
}

export interface StreamEvent {
  event: 'node_start' | 'node_complete' | 'token' | 'synthesis_complete' | 'complete' | 'error'
  data: any
}
