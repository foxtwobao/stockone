import { FormEvent, useEffect, useState } from 'react'
import { Logo } from './Logo'
import { api } from '@/lib/api'
import { getAccessKey, setAccessKey } from '@/lib/auth'

export function AuthGate({ children }: { children: React.ReactNode }) {
  const [checking, setChecking] = useState(true)
  const [enabled, setEnabled] = useState(false)
  const [unlocked, setUnlocked] = useState(false)
  const [key, setKey] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    let alive = true
    async function check() {
      try {
        const status = await api.authStatus()
        if (!alive) return
        setEnabled(status.enabled)
        if (!status.enabled) {
          setUnlocked(true)
          return
        }
        const saved = getAccessKey()
        if (saved) {
          await api.authLogin(saved)
          if (alive) setUnlocked(true)
        }
      } catch {
        if (alive) setError('访问 Key 已失效，请重新输入')
      } finally {
        if (alive) setChecking(false)
      }
    }
    check()
    return () => { alive = false }
  }, [])

  async function submit(e: FormEvent) {
    e.preventDefault()
    const trimmed = key.trim()
    if (!trimmed) {
      setError('请输入访问 Key')
      return
    }
    setSubmitting(true)
    setError('')
    try {
      await api.authLogin(trimmed)
      setAccessKey(trimmed)
      setUnlocked(true)
    } catch {
      setError('访问 Key 不正确')
    } finally {
      setSubmitting(false)
    }
  }

  if (checking) {
    return (
      <div className="min-h-screen bg-base grid place-items-center text-muted">
        <div className="flex flex-col items-center gap-3">
          <Logo size={30} className="text-foreground" />
          <div className="text-xs">加载中…</div>
        </div>
      </div>
    )
  }

  if (!enabled || unlocked) return <>{children}</>

  return (
    <div className="min-h-screen bg-base text-foreground grid place-items-center px-6">
      <form onSubmit={submit} className="w-full max-w-sm rounded-card border border-border bg-surface p-6">
        <div className="flex items-center gap-3">
          <Logo size={30} className="text-bear" />
          <div>
            <div className="font-mono text-sm font-bold tracking-[0.08em]">StockOne</div>
            <div className="mt-0.5 text-[10px] uppercase tracking-[0.2em] text-muted">Quant Terminal</div>
          </div>
        </div>

        <label className="mt-6 block text-xs font-medium text-secondary" htmlFor="stockone-access-key">
          访问 Key
        </label>
        <input
          id="stockone-access-key"
          type="password"
          value={key}
          onChange={(e) => setKey(e.target.value)}
          autoFocus
          className="mt-2 w-full rounded-btn border border-border bg-base px-3 py-2 text-sm text-foreground outline-none transition-colors focus:border-accent"
        />
        {error && <div className="mt-2 text-xs text-danger">{error}</div>}
        <button
          type="submit"
          disabled={submitting}
          className="mt-5 w-full rounded-btn bg-accent px-3 py-2 text-sm font-medium text-base transition-opacity disabled:opacity-60"
        >
          {submitting ? '验证中…' : '进入'}
        </button>
      </form>
    </div>
  )
}
