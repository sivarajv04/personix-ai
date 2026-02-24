const API = import.meta.env.VITE_API_URL;

export async function requestDataset(data) {
  const res = await fetch(`${BASE_URL}/dataset/request`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Request failed");

  const json = await res.json();

  // extract passcode from message
  const passcodeMatch = json.message.match(/(\d{6})$/);
  const passcode = passcodeMatch ? passcodeMatch[1] : null;

  return {
    request_id: json.request_id,
    passcode,
    status: json.status,
  };
}
