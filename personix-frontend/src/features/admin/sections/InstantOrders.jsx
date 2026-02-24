import { useEffect, useState } from "react";
import { getInstantOrders } from "../api/admin";

export default function InstantOrders() {

  const [orders, setOrders] = useState(null);

  useEffect(() => {
    getInstantOrders()
      .then(setOrders)
      .catch(() => setOrders([]));
  }, []);

  if (!orders) return <p className="text-zinc-400">Loading instant orders...</p>;

  if (orders.length === 0)
    return <p className="text-zinc-500">No instant orders yet</p>;

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5">

      <h2 className="text-xl mb-4">Instant Orders</h2>

      <table className="w-full text-sm">
        <thead className="text-zinc-400 border-b border-zinc-800">
          <tr>
            <th className="text-left py-2">Request ID</th>
            <th className="text-left">Gender</th>
            <th className="text-left">Age</th>
            <th className="text-left">Count</th>
            <th className="text-left">Status</th>
          </tr>
        </thead>

        <tbody>
          {orders.map((o) => (
            <tr key={o.request_id} className="border-b border-zinc-800">
              <td className="py-2">{o.request_id}</td>
              <td>{o.gender}</td>
              <td>{o.age_bucket}</td>
              <td>{o.count}</td>
              <td className={
                o.status === "completed"
                  ? "text-green-400"
                  : "text-yellow-400"
              }>
                {o.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
}
