import { useEffect, useState } from "react";
import { checkBackend } from "../../api/system";

export default function BackendStatus() {

  const [online, setOnline] = useState(null);

  useEffect(() => {
    const ping = async () => {
      const ok = await checkBackend();
      setOnline(ok);
    };

    ping();
    const interval = setInterval(ping, 5000); // every 5 sec
    return () => clearInterval(interval);
  }, []);

  if (online === null) return null;

  return (
    <div className="flex items-center gap-2 text-sm">
      <div
        className={`w-2.5 h-2.5 rounded-full ${
          online ? "bg-green-500" : "bg-red-500"
        }`}
      />
      <span className="text-zinc-400">
        {online ? "Backend Connected" : "Backend Offline"}
      </span>
    </div>
  );
}
