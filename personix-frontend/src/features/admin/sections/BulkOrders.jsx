import { useEffect, useState } from "react";
import { getBulkOrders } from "../api/admin";

export default function BulkOrders() {

  const [orders, setOrders] = useState([]);

  useEffect(() => {
    getBulkOrders().then(setOrders).catch(console.error);
  }, []);

  return (
    <div>
      <h1 className="text-2xl mb-6">Bulk Orders</h1>

      <div className="border border-zinc-800 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-zinc-900 text-zinc-400">
            <tr>
              <th className="p-3 text-left">Client</th>
              <th className="p-3 text-left">Contact</th>
              <th className="p-3 text-left">Groups</th>
              <th className="p-3 text-left">Status</th>
              <th className="p-3 text-left">Date</th>
            </tr>
          </thead>

          <tbody>
            {orders.map(o => (
              <tr key={o.id} className="border-t border-zinc-800">
                <td className="p-3">{o.name}</td>
                <td className="p-3">{o.email}</td>
                <td className="p-3">{o.dataset_groups?.length || 0}</td>
                <td className="p-3 text-yellow-400">{o.status}</td>
                <td className="p-3">{new Date(o.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
