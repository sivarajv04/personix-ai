import { useEffect, useState } from "react";
import { getSystemHealth } from "../api/admin";
import SystemStatusCard from "../components/SystemStatusCard";

export default function SystemMonitor() {

  const [health, setHealth] = useState(null);

  const load = () => {
    getSystemHealth()
      .then(setHealth)
      .catch(() => setHealth(null));
  };

  useEffect(() => {
    load();
    const i = setInterval(load, 5000);
    return () => clearInterval(i);
  }, []);

  return (
    <div className="space-y-8">

      <h1 className="text-3xl mb-4">System Monitor</h1>

      <SystemStatusCard health={health} />

      {health && (
        <div className="grid grid-cols-2 gap-6">

          <DebugCard title="Queue Raw Data" data={health.queue} />
          <DebugCard title="Performance Raw Data" data={health.performance} />
          <DebugCard title="Downloads Raw Data" data={health.downloads} />
          <DebugCard title="Worker Raw Data" data={health.worker} />

        </div>
      )}

    </div>
  );
}

function DebugCard({ title, data }) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
      <h2 className="text-xl mb-4">{title}</h2>
      <pre className="text-xs text-zinc-400 overflow-auto">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}