import { useEffect, useState } from "react";
import { getDailyUsage } from "../api/admin";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

export default function UsageChart() {

  const [data, setData] = useState([]);

  useEffect(() => {
    getDailyUsage().then(setData).catch(console.error);
  }, []);

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
      <h2 className="text-lg mb-4">Daily Orders</h2>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="#27272a" />
            <XAxis dataKey="date" stroke="#a1a1aa" />
            <YAxis stroke="#a1a1aa" />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="orders"
              stroke="#22c55e"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
