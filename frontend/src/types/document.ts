export interface DocumentType {
  id: number
  filename: string
  original_filename: string
  file_type: string
  file_size: number
  chunks_count: number | null
  uploaded_at: string
  is_ingested: boolean
  ingestion_status: 'pending' | 'processing' | 'completed' | 'failed'
  error_message: string | null
}

export interface DocumentStats {
  total_documents: number
  total_size_mb: number
  total_chunks: number
  by_type: Record<string, number>
}
