import { useEffect, useRef } from 'react'
import { useChatStore } from '../../stores/chatStore'
import { useSSE } from '../../hooks/useSSE'
import { chatApi, sessionsApi } from '../../lib/api'
import MessageItem from './MessageItem'
import MessageInput from './MessageInput'
import StreamingMessage from './StreamingMessage'
import { ScrollArea } from '../ui/scroll-area'
import { Loader2 } from 'lucide-react'

interface ChatInterfaceProps {
  sessionId: number
  onShowSources?: (sources: string[]) => void
}

export default function ChatInterface({ sessionId, onShowSources }: ChatInterfaceProps) {
  const {
    messages,
    isStreaming,
    streamingContent,
    currentNode,
    setMessages,
    addMessage,
    setIsStreaming,
    setStreamingContent,
    setCurrentNode,
  } = useChatStore()

  const { startStream } = useSSE()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadMessages()
  }, [sessionId])

  useEffect(() => {
    // Auto-scroll to bottom
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, streamingContent])

  const loadMessages = async () => {
    try {
      const response = await sessionsApi.get(sessionId)
      setMessages(response.data.messages)
    } catch (error) {
      console.error('Error loading messages:', error)
    }
  }

  const handleSendMessage = (query: string) => {
    // Add user message
    addMessage({
      id: Date.now(),
      session_id: sessionId,
      role: 'user',
      content: query,
      created_at: new Date().toISOString(),
    })

    // Start streaming
    setIsStreaming(true)
    setStreamingContent('')
    setCurrentNode('query_analysis')

    const streamUrl = chatApi.getStreamUrl(sessionId, query)

    startStream(streamUrl, {
      onNodeStart: (data) => {
        setCurrentNode(data.node)
      },
      onToken: (data) => {
        setStreamingContent(data.partial_response)
      },
      onSynthesisComplete: (data) => {
        setStreamingContent(data.content)

        addMessage({
          id: Date.now(),
          session_id: sessionId,
          role: 'assistant',
          content: data.content,
          sources: data.sources,
          documents_used: data.documents_used,
          relevance_score: data.relevance_score,
          iterations: data.iterations,
          created_at: new Date().toISOString(),
        })

        if (data.sources?.length > 0) {
          onShowSources?.(data.sources)
        }
      },
      onComplete: () => {
        setIsStreaming(false)
        setStreamingContent('')
        setCurrentNode('')
      },
      onError: (error) => {
        console.error('Streaming error:', error)
        setIsStreaming(false)
        setStreamingContent('')
        setCurrentNode('')
        alert('Error: ' + (error.error || 'Unknown error'))
      },
    })
  }

  return (
    <div className="flex flex-col h-full">
      <ScrollArea ref={scrollAreaRef} className="flex-1 p-4">
        {messages.length === 0 && !isStreaming ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <div className="text-center">
              <p className="text-lg font-medium">Start a conversation</p>
              <p className="text-sm mt-1">Ask a research question to begin</p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <MessageItem
                key={message.id}
                message={message}
                onShowSources={onShowSources}
              />
            ))}

            {isStreaming && (
              <StreamingMessage content={streamingContent} currentNode={currentNode} />
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </ScrollArea>

      <MessageInput onSend={handleSendMessage} disabled={isStreaming} />
    </div>
  )
}
