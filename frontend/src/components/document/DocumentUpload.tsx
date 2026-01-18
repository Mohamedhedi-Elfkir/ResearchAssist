import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, Loader2 } from 'lucide-react'
import { documentsApi } from '../../lib/api'
import { useDocumentStore } from '../../stores/documentStore'

export default function DocumentUpload() {
  const [uploading, setUploading] = useState(false)
  const addDocument = useDocumentStore(state => state.addDocument)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setUploading(true)

    try {
      for (const file of acceptedFiles) {
        const response = await documentsApi.upload(file)
        addDocument(response.data)
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('Failed to upload document')
    } finally {
      setUploading(false)
    }
  }, [addDocument])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md']
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    disabled: uploading
  })

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-lg p-6 text-center cursor-pointer
        transition-colors
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
        ${uploading ? 'pointer-events-none opacity-50' : ''}
      `}
    >
      <input {...getInputProps()} />

      <div className="flex flex-col items-center gap-2">
        {uploading ? (
          <>
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
            <p className="text-sm text-gray-600">Uploading and processing...</p>
          </>
        ) : isDragActive ? (
          <>
            <Upload className="w-8 h-8 text-blue-500" />
            <p className="text-sm text-gray-600">Drop files here</p>
          </>
        ) : (
          <>
            <FileText className="w-8 h-8 text-gray-400" />
            <p className="text-sm text-gray-600">
              Drag & drop files or click to browse
            </p>
            <p className="text-xs text-gray-500">
              Supports PDF, TXT, MD (max 50MB)
            </p>
          </>
        )}
      </div>
    </div>
  )
}
