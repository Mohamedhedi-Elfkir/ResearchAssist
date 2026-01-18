import { FileText, Trash2, CheckCircle, XCircle, Loader2 } from 'lucide-react'
import type { DocumentType } from '../../types/document'
import { Button } from '../ui/button'
import { documentsApi } from '../../lib/api'
import { useDocumentStore } from '../../stores/documentStore'

interface DocumentItemProps {
  document: DocumentType
}

export default function DocumentItem({ document }: DocumentItemProps) {
  const removeDocument = useDocumentStore(state => state.removeDocument)

  const handleDelete = async () => {
    if (!confirm(`Delete ${document.original_filename}?`)) return

    try {
      await documentsApi.delete(document.id)
      removeDocument(document.id)
    } catch (error) {
      console.error('Delete error:', error)
      alert('Failed to delete document')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const getStatusIcon = () => {
    switch (document.ingestion_status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-500" />
      case 'processing':
        return <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
      default:
        return <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
    }
  }

  return (
    <div className="flex items-center gap-3 p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors">
      <FileText className="w-5 h-5 text-muted-foreground flex-shrink-0" />

      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate" title={document.original_filename}>
          {document.original_filename}
        </p>
        <div className="flex items-center gap-2 mt-1">
          <span className="text-xs text-muted-foreground">
            {formatFileSize(document.file_size)}
          </span>
          {document.chunks_count && (
            <span className="text-xs text-muted-foreground">
              • {document.chunks_count} chunks
            </span>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2 flex-shrink-0">
        {getStatusIcon()}
        <Button
          variant="ghost"
          size="icon"
          onClick={handleDelete}
          className="h-8 w-8"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>
    </div>
  )
}
