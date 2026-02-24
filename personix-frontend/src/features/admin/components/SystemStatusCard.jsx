import React from "react";

export default function SystemStatusCard({ health }) {

  if (!health || !health.queue || !health.performance || !health.downloads) {
    return (
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
        <h2 className="text-xl mb-4">System Status</h2>
        <p className="text-red-400">Monitoring offline</p>
      </div>
    );
  }

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">

      <h2 className="text-xl mb-6">System Status</h2>

      <div className="grid grid-cols-3 gap-6 text-sm">

        <Status label="Database" value={health.db_status} good="online" />

        <Status
          label="Pending Jobs"
          value={health.queue.pending_jobs}
          good={0}
          invert
        />

        <Status
          label="Oldest Waiting (sec)"
          value={Math.floor(health.queue.oldest_pending_seconds)}
          good={60}
          invert
        />

        <Status
          label="Avg Generation Time (sec)"
          value={Math.floor(health.performance.avg_completion_seconds)}
          good={20}
          invert
        />

        <Status
          label="Unused Completed Orders"
          value={health.downloads.unused_completed_orders}
          good={5}
          invert
        />

      </div>
    </div>
  );
}

function Status({ label, value, good, invert }) {

  let color = "text-green-400";

  if (invert) {
    if (value > good) color = "text-yellow-400";
    if (value > good * 3) color = "text-red-400";
  } else {
    if (value !== good) color = "text-red-400";
  }

  return (
    <div className="flex flex-col">
      <span className="text-zinc-400">{label}</span>
      <span className={`text-lg ${color}`}>{value}</span>
    </div>
  );
}