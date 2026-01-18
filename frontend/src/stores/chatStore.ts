import { create } from 'zustand'
import type { Message, Session } from '../types/chat'

interface ChatState {
  currentSession: Session | null
  messages: Message[]
  isStreaming: boolean
  streamingContent: string
  currentNode: string

  setCurrentSession: (session: Session | null) => void
  setMessages: (messages: Message[]) => void
  addMessage: (message: Message) => void
  setIsStreaming: (streaming: boolean) => void
  setStreamingContent: (content: string) => void
  setCurrentNode: (node: string) => void
  clearMessages: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  currentSession: null,
  messages: [],
  isStreaming: false,
  streamingContent: '',
  currentNode: '',

  setCurrentSession: (session) => set({ currentSession: session }),
  setMessages: (messages) => set({ messages }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setIsStreaming: (streaming) => set({ isStreaming: streaming }),
  setStreamingContent: (content) => set({ streamingContent: content }),
  setCurrentNode: (node) => set({ currentNode: node }),
  clearMessages: () => set({ messages: [], streamingContent: '', currentNode: '' }),
}))
