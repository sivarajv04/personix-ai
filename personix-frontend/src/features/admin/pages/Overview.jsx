import { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import SystemStatusCard from "../components/SystemStatusCard";
import { getMetrics, getSystemHealth } from "../api/admin";

export default function Overview() {

  const [stats, setStats] = useState(null);
  const [health, setHealth] = useState(null);

  // load dashboard stats
  useEffect(() => {
    getMetrics().then(setStats).catch(() => setStats(null));
  }, []);

  // load monitoring data (auto refresh every 5s)
  useEffect(() => {

    const loadHealth = () => {
      getSystemHealth().then(setHealth).catch(() => setHealth(null));
    };

    loadHealth(); // first load
    const interval = setInterval(loadHealth, 5000);

    return () => clearInterval(interval);

  }, []);

  return (
    <div>

      <h1 className="text-3xl mb-8">Dashboard</h1>



      {/* ORDER METRICS */}
      <div className="grid grid-cols-4 gap-6 mt-8">

        <StatCard title="Total Orders" value={stats?.total_orders ?? "--"} />
        <StatCard title="Pending" value={stats?.pending_orders ?? "--"} />
        <StatCard title="Completed" value={stats?.completed_orders ?? "--"} />
        <StatCard title="Today" value={stats?.today_orders ?? "--"} />

      </div>

    </div>
  );
}
// import StatCard from "../components/StatCard";

// export default function Overview() {
//   return (
//     <div>

//       <h1 className="text-3xl mb-8">Dashboard</h1>

//       <div className="grid grid-cols-4 gap-6">

//         <StatCard title="Total Orders" value="--" />
//         <StatCard title="Pending" value="--" />
//         <StatCard title="Completed" value="--" />
//         <StatCard title="Bulk Requests" value="--" />

//       </div>

//     </div>
//   );
// }
