const API = import.meta.env.VITE_API_URL;

export async function checkBackend() {
  try {
    const res = await fetch(`${API}/health`, { method: "GET" });
    return res.ok;
  } catch {
    return false;
  }
}
