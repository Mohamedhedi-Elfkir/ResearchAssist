import type { Message } from '../../types/chat'
import { User, Bot, FileText } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface MessageItemProps {
  message: Message
  onShowSources?: (sources: string[]) => void
}

export default function MessageItem({ message, onShowSources }: MessageItemProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 p-4 ${isUser ? 'bg-muted/30' : ''}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-blue-500' : 'bg-green-500'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      <div className="flex-1 min-w-0">
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-3 border-t">
            <button
              onClick={() => onShowSources?.(message.sources!)}
              className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              <FileText className="w-4 h-4" />
              <span>{message.sources.length} source{message.sources.length > 1 ? 's' : ''}</span>
              {message.relevance_score && (
                <span className="text-xs">
                  (relevance: {message.relevance_score.toFixed(1)}/10)
                </span>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
