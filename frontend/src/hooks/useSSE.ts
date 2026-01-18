import { useCallback } from 'react'

interface SSECallbacks {
  onNodeStart?: (data: { node: string }) => void
  onNodeComplete?: (data: { node: string }) => void
  onToken?: (data: { token: string; partial_response: string }) => void
  onSynthesisComplete?: (data: {
    content: string
    sources: string[]
    documents_used: number
    relevance_score: number
    iterations: number
  }) => void
  onComplete?: (data: { message_id: number }) => void
  onError?: (error: any) => void
}

export function useSSE() {
  const startStream = useCallback((url: string, callbacks: SSECallbacks) => {
    const eventSource = new EventSource(url)

    eventSource.addEventListener('node_start', (e) => {
      try {
        const data = JSON.parse(e.data)
        callbacks.onNodeStart?.(data)
      } catch (err) {
        console.error('Error parsing node_start:', err)
      }
    })

    eventSource.addEventListener('node_complete', (e) => {
      try {
        const data = JSON.parse(e.data)
        callbacks.onNodeComplete?.(data)
      } catch (err) {
        console.error('Error parsing node_complete:', err)
      }
    })

    eventSource.addEventListener('token', (e) => {
      try {
        const data = JSON.parse(e.data)
        callbacks.onToken?.(data)
      } catch (err) {
        console.error('Error parsing token:', err)
      }
    })

    eventSource.addEventListener('synthesis_complete', (e) => {
      try {
        const data = JSON.parse(e.data)
        callbacks.onSynthesisComplete?.(data)
      } catch (err) {
        console.error('Error parsing synthesis_complete:', err)
      }
    })

    eventSource.addEventListener('complete', (e) => {
      try {
        const data = JSON.parse(e.data)
        callbacks.onComplete?.(data)
        eventSource.close()
      } catch (err) {
        console.error('Error parsing complete:', err)
        eventSource.close()
      }
    })

    eventSource.addEventListener('error', (e: any) => {
      try {
        const data = e.data ? JSON.parse(e.data) : { error: 'Unknown error' }
        callbacks.onError?.(data)
      } catch (err) {
        callbacks.onError?.({ error: 'Connection error' })
      }
      eventSource.close()
    })

    eventSource.onerror = () => {
      callbacks.onError?.({ error: 'Connection failed' })
      eventSource.close()
    }

    // Return cleanup function
    return () => eventSource.close()
  }, [])

  return { startStream }
}
