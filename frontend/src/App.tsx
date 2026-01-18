import { useState } from 'react'
import Sidebar from './components/layout/Sidebar'
import SourcePanel from './components/layout/SourcePanel'
import ChatInterface from './components/chat/ChatInterface'
import { useChatStore } from './stores/chatStore'

function App() {
  const [showSourcePanel, setShowSourcePanel] = useState(false)
  const [currentSources, setCurrentSources] = useState<string[]>([])
  const currentSession = useChatStore(state => state.currentSession)

  const handleShowSources = (sources: string[]) => {
    setCurrentSources(sources)
    setShowSourcePanel(true)
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Left Sidebar - Documents & Sessions */}
      <Sidebar />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {currentSession ? (
          <>
            <div className="flex items-center justify-between p-4 border-b bg-background">
              <h1 className="text-xl font-semibold">{currentSession.title}</h1>
            </div>
            <ChatInterface
              sessionId={currentSession.id}
              onShowSources={handleShowSources}
            />
          </>
        ) : (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-2">Research Agent</h2>
              <p className="text-sm">Create a new chat to get started</p>
            </div>
          </div>
        )}
      </div>

      {/* Right Panel - Sources (collapsible) */}
      {showSourcePanel && (
        <SourcePanel
          sources={currentSources}
          onClose={() => setShowSourcePanel(false)}
        />
      )}
    </div>
  )
}

export default App
