import { X, FileText } from 'lucide-react'
import { Button } from '../ui/button'
import { ScrollArea } from '../ui/scroll-area'

interface SourcePanelProps {
  sources: string[]
  onClose: () => void
}

export default function SourcePanel({ sources, onClose }: SourcePanelProps) {
  const getFileName = (path: string) => {
    return path.split(/[\\/]/).pop() || path
  }

  return (
    <div className="w-80 border-l bg-background flex flex-col h-screen">
      <div className="flex items-center justify-between p-4 border-b">
        <h2 className="text-lg font-semibold">Sources</h2>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="w-4 h-4" />
        </Button>
      </div>

      <ScrollArea className="flex-1 p-4">
        <div className="space-y-2">
          {sources.map((source, index) => (
            <div
              key={index}
              className="flex items-start gap-3 p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
            >
              <FileText className="w-5 h-5 text-muted-foreground flex-shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium break-all">
                  {getFileName(source)}
                </p>
                <p className="text-xs text-muted-foreground mt-1 break-all">
                  {source}
                </p>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}
