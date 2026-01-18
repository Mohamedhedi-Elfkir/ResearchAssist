import { FileText, MessageSquare } from 'lucide-react'
import { Card } from '../ui/card'
import DocumentUpload from '../document/DocumentUpload'
import DocumentList from '../document/DocumentList'
import SessionList from '../session/SessionList'
import { useState } from 'react'

export default function Sidebar() {
  const [activeTab, setActiveTab] = useState<'documents' | 'sessions'>('sessions')

  return (
    <div className="w-80 border-r bg-background flex flex-col h-screen">
      {/* Tab Switcher */}
      <div className="flex border-b">
        <button
          onClick={() => setActiveTab('sessions')}
          className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium transition-colors ${
            activeTab === 'sessions'
              ? 'bg-accent text-accent-foreground border-b-2 border-primary'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          Chats
        </button>
        <button
          onClick={() => setActiveTab('documents')}
          className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium transition-colors ${
            activeTab === 'documents'
              ? 'bg-accent text-accent-foreground border-b-2 border-primary'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <FileText className="w-4 h-4" />
          Documents
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {activeTab === 'sessions' ? (
          <SessionList />
        ) : (
          <div className="flex flex-col h-full">
            <div className="p-4 border-b">
              <DocumentUpload />
            </div>
            <div className="flex-1 p-4 overflow-hidden">
              <DocumentList />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
