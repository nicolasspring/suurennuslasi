const API_URL = import.meta.env.VITE_API_URL;

export async function apiFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`);

  if (!response.ok) {
    throw new Error("API request failed");
  }

  return response.json();
}
