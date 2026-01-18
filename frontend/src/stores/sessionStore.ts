import { create } from 'zustand'
import type { Session } from '../types/chat'

interface SessionState {
  sessions: Session[]
  isLoading: boolean

  setSessions: (sessions: Session[]) => void
  addSession: (session: Session) => void
  updateSession: (id: number, updates: Partial<Session>) => void
  removeSession: (id: number) => void
  setIsLoading: (loading: boolean) => void
}

export const useSessionStore = create<SessionState>((set) => ({
  sessions: [],
  isLoading: false,

  setSessions: (sessions) => set({ sessions }),
  addSession: (session) => set((state) => ({ sessions: [session, ...state.sessions] })),
  updateSession: (id, updates) => set((state) => ({
    sessions: state.sessions.map(s => s.id === id ? { ...s, ...updates } : s)
  })),
  removeSession: (id) => set((state) => ({
    sessions: state.sessions.filter(s => s.id !== id)
  })),
  setIsLoading: (loading) => set({ isLoading: loading }),
}))
