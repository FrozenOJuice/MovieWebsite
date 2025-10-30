// Simple centralized API utility for WatchWorthy frontend

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export async function postData(endpoint: string, data: any) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  const result = await response.json()
  if (!response.ok) {
    throw new Error(result.detail || 'Request failed')
  }
  return result
}
