import { Bot, Loader2 } from 'lucide-react'

interface StreamingMessageProps {
  content: string
  currentNode: string
}

const nodeLabels: Record<string, string> = {
  query_analysis: 'Analyzing query',
  research_planning: 'Planning research',
  rag_retrieval: 'Searching documents',
  relevance_check: 'Checking relevance',
  web_scraping: 'Web search',
  synthesis: 'Generating answer',
}

export default function StreamingMessage({ content, currentNode }: StreamingMessageProps) {
  return (
    <div className="flex gap-3 p-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-green-500">
        <Bot className="w-5 h-5 text-white" />
      </div>

      <div className="flex-1 min-w-0">
        {currentNode && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
            <Loader2 className="w-3 h-3 animate-spin" />
            <span>{nodeLabels[currentNode] || currentNode}</span>
          </div>
        )}

        <div className="prose prose-sm max-w-none whitespace-pre-wrap">
          {content}
          {content && <span className="inline-block w-1 h-4 bg-current animate-pulse ml-1" />}
        </div>
      </div>
    </div>
  )
}
