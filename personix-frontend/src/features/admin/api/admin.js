const API = import.meta.env.VITE_API_URL;
// ---------------- METRICS ----------------
export async function getMetrics() {
  const res = await fetch(`${API}/admin/metrics`);
  if (!res.ok) throw new Error("Failed to fetch metrics");
  return res.json();
}

// ---------------- INSTANT ORDERS ----------------
export async function getInstantOrders() {
  const res = await fetch(`${API}/admin/dataset-orders`);
  if (!res.ok) throw new Error("Failed to fetch dataset orders");
  return res.json();
}

// ---------------- BULK ORDERS ----------------
export async function getBulkOrders() {
  const res = await fetch(`${API}/admin/bulk-orders`);
  if (!res.ok) throw new Error("Failed to fetch bulk orders");
  return res.json();
}

// ---------------- INVENTORY ----------------
export async function getInventory() {
  const res = await fetch(`${API}/admin/inventory`);
  if (!res.ok) throw new Error("Failed to fetch inventory");
  return res.json();
}

// ---------------- UPDATE STATUS ----------------
export async function updateOrderStatus(id, status) {
  const res = await fetch(`${API}/admin/order-status/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });

  if (!res.ok) throw new Error("Failed to update status");
  return res.json();
}

export async function getDailyUsage() {
  const res = await fetch(`${API}/admin/usage-daily`);
  if (!res.ok) throw new Error("Failed to fetch usage");
  return res.json();
}

// ---------------- SYSTEM HEALTH ----------------
export async function getSystemHealth() {
  const res = await fetch(`${API}/admin/system-health`);
  return await res.json();
}

// const API = "http://127.0.0.1:8000/admin";

// // ---------------- LOGIN ----------------
// export async function adminLogin(password) {
//   const res = await fetch(`${API}/login`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ password })
//   });

//   if (!res.ok) throw new Error("Invalid password");
//   return res.json();
// }

// // ---------------- METRICS ----------------
// export async function getMetrics() {
//   const res = await fetch(`${API}/metrics`);
//   if (!res.ok) throw new Error("Failed to fetch metrics");
//   return res.json();
// }

// // ---------------- INSTANT ORDERS ----------------
// export async function getInstantOrders() {
//   const res = await fetch(`${API}/dataset-orders`);
//   if (!res.ok) throw new Error("Failed to fetch dataset orders");
//   return res.json();
// }

// // ---------------- BULK ORDERS ----------------
// export async function getBulkOrders() {
//   const res = await fetch(`${API}/bulk-orders`);
//   if (!res.ok) throw new Error("Failed to fetch bulk orders");
//   return res.json();
// }

// // ---------------- INVENTORY ----------------
// export async function getInventory() {
//   const res = await fetch(`${API}/inventory`);
//   if (!res.ok) throw new Error("Failed to fetch inventory");
//   return res.json();
// }


// const API = "http://127.0.0.1:8000";

// // ---------------- DATASET ORDERS ----------------
// export async function getInstantOrders() {
//   const res = await fetch(`${API}/admin/dataset-orders`);
//   if (!res.ok) throw new Error("Failed to fetch dataset orders");
//   return res.json();
// }

// // ---------------- BULK ORDERS ----------------
// export async function getBulkOrders() {
//   const res = await fetch(`${API}/admin/bulk-orders`);
//   if (!res.ok) throw new Error("Failed to fetch bulk orders");
//   return res.json();
// }

// // ---------------- INVENTORY ----------------
// export async function getInventory() {
//   const res = await fetch(`${API}/admin/inventory`);
//   if (!res.ok) throw new Error("Failed to fetch inventory");
//   return res.json();
// }

// // ---------------- METRICS ----------------
// export async function getMetrics() {
//   const res = await fetch(`${API}/admin/metrics`);
//   if (!res.ok) throw new Error("Failed to fetch metrics");
//   return res.json();
// }
