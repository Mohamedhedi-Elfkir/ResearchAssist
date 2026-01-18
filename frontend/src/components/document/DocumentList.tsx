import { useEffect } from 'react'
import { documentsApi } from '../../lib/api'
import { useDocumentStore } from '../../stores/documentStore'
import DocumentItem from './DocumentItem'
import { ScrollArea } from '../ui/scroll-area'
import { Loader2 } from 'lucide-react'

export default function DocumentList() {
  const { documents, isLoading, setDocuments, setIsLoading } = useDocumentStore()

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    setIsLoading(true)
    try {
      const response = await documentsApi.list()
      setDocuments(response.data.documents)
    } catch (error) {
      console.error('Error loading documents:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
      </div>
    )
  }

  if (documents.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <p className="text-sm">No documents yet</p>
        <p className="text-xs mt-1">Upload documents to get started</p>
      </div>
    )
  }

  return (
    <ScrollArea className="h-full">
      <div className="space-y-2">
        {documents.map(doc => (
          <DocumentItem key={doc.id} document={doc} />
        ))}
      </div>
    </ScrollArea>
  )
}
