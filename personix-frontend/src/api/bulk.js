const API = import.meta.env.VITE_API_URL;

export async function submitBulkOrder(data) {
  const res = await fetch(`${API}/bulk/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  if (!res.ok) {
    throw new Error("Failed to submit bulk order");
  }

  return await res.json();
}
