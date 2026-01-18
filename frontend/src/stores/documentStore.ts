import { create } from 'zustand'
import type { DocumentType, DocumentStats } from '../types/document'

interface DocumentState {
  documents: DocumentType[]
  stats: DocumentStats | null
  isLoading: boolean

  setDocuments: (documents: DocumentType[]) => void
  addDocument: (document: DocumentType) => void
  removeDocument: (id: number) => void
  setStats: (stats: DocumentStats) => void
  setIsLoading: (loading: boolean) => void
}

export const useDocumentStore = create<DocumentState>((set) => ({
  documents: [],
  stats: null,
  isLoading: false,

  setDocuments: (documents) => set({ documents }),
  addDocument: (document) => set((state) => ({ documents: [...state.documents, document] })),
  removeDocument: (id) => set((state) => ({
    documents: state.documents.filter(doc => doc.id !== id)
  })),
  setStats: (stats) => set({ stats }),
  setIsLoading: (loading) => set({ isLoading: loading }),
}))
