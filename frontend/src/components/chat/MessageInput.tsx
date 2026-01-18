import { useState } from 'react'
import { Send } from 'lucide-react'
import { Button } from '../ui/button'
import { Input } from '../ui/input'

interface MessageInputProps {
  onSend: (message: string) => void
  disabled?: boolean
}

export default function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input.trim())
      setInput('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t bg-background">
      <div className="flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a research question..."
          disabled={disabled}
          className="flex-1"
        />
        <Button type="submit" disabled={disabled || !input.trim()} size="icon">
          <Send className="w-4 h-4" />
        </Button>
      </div>
    </form>
  )
}
