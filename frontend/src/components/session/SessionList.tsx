import { useEffect } from 'react'
import { Plus, MessageSquare } from 'lucide-react'
import { Button } from '../ui/button'
import { ScrollArea } from '../ui/scroll-area'
import { sessionsApi } from '../../lib/api'
import { useSessionStore } from '../../stores/sessionStore'
import { useChatStore } from '../../stores/chatStore'

export default function SessionList() {
  const { sessions, setSessions, addSession, setIsLoading } = useSessionStore()
  const { currentSession, setCurrentSession, clearMessages } = useChatStore()

  useEffect(() => {
    loadSessions()
  }, [])

  const loadSessions = async () => {
    setIsLoading(true)
    try {
      const response = await sessionsApi.list()
      setSessions(response.data.sessions)

      // Select first session if none selected
      if (!currentSession && response.data.sessions.length > 0) {
        setCurrentSession(response.data.sessions[0])
      }
    } catch (error) {
      console.error('Error loading sessions:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateSession = async () => {
    try {
      const response = await sessionsApi.create('New Research Session')
      const newSession = response.data
      addSession(newSession)
      setCurrentSession(newSession)
      clearMessages()
    } catch (error) {
      console.error('Error creating session:', error)
      alert('Failed to create session')
    }
  }

  const handleSelectSession = (session: any) => {
    setCurrentSession(session)
    clearMessages()
  }

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b">
        <Button onClick={handleCreateSession} className="w-full" size="sm">
          <Plus className="w-4 h-4 mr-2" />
          New Chat
        </Button>
      </div>

      <ScrollArea className="flex-1 p-2">
        {sessions.length === 0 ? (
          <div className="text-center py-8 px-4 text-muted-foreground text-sm">
            No conversations yet
          </div>
        ) : (
          <div className="space-y-1">
            {sessions.map((session) => (
              <button
                key={session.id}
                onClick={() => handleSelectSession(session)}
                className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                  currentSession?.id === session.id
                    ? 'bg-accent text-accent-foreground'
                    : 'hover:bg-accent/50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{session.title}</p>
                    <p className="text-xs text-muted-foreground">
                      {session.message_count} message{session.message_count !== 1 ? 's' : ''}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  )
}
