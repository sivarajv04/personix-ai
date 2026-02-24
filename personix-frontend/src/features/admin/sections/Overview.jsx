import { useEffect, useState } from "react";
import { getMetrics } from "../api/admin";
import StatCard from "../components/StatCard";
import UsageChart from "../components/UsageChart";

export default function Overview() {

  const [stats, setStats] = useState(null);

  useEffect(() => {
    getMetrics()
      .then(setStats)
      .catch(() => setStats(null));
  }, []);

  if (!stats) {
    return <p className="text-zinc-400">Loading metrics...</p>;
  }

  return (
    <div className="space-y-10">

      {/* KPI CARDS */}
      <div className="grid grid-cols-4 gap-6">
        <StatCard title="Total Orders" value={stats.total_orders} />
        <StatCard title="Pending" value={stats.pending_orders} />
        <StatCard title="Completed" value={stats.completed_orders} />
        <StatCard title="Today" value={stats.today_orders} />
      </div>

      {/* CHART */}
      <UsageChart />

    </div>
  );

}

// export default function Overview() {
//   return (
//     <div className="text-white">
//       Admin Overview
//     </div>
//   );
// }
