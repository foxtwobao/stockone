export const AUTH_HEADER = 'X-StockOne-Key'
export const AUTH_QUERY = 'access_key'

const STORAGE_KEY = 'stockone_access_key'

export function getAccessKey(): string {
  try {
    return localStorage.getItem(STORAGE_KEY) || ''
  } catch {
    return ''
  }
}

export function setAccessKey(key: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, key)
  } catch {
    // ignore
  }
}

export function clearAccessKey(): void {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    // ignore
  }
}

export function authHeaders(): Record<string, string> {
  const key = getAccessKey()
  return key ? { [AUTH_HEADER]: key } : {}
}

export function withAccessKey(url: string): string {
  const key = getAccessKey()
  if (!key) return url
  const sep = url.includes('?') ? '&' : '?'
  return `${url}${sep}${AUTH_QUERY}=${encodeURIComponent(key)}`
}
