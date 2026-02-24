// import { useState } from "react";

// const API = "http://127.0.0.1:8000";

// export default function TrackCard() {

//   const [rid, setRid] = useState("");
//   const [status, setStatus] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const checkStatus = async () => {

//     if (!rid) {
//       setStatus({ error: "Enter a request ID" });
//       return;
//     }

//     setLoading(true);
//     setStatus(null);

//     try {
//       const res = await fetch(`${API}/dataset/status/${rid}`);
//       const data = await res.json();

//       if (!res.ok) {
//         setStatus({ error: data.detail || "Request not found" });
//         setLoading(false);
//         return;
//       }

//       setStatus(data);

//     } catch {
//       setStatus({ error: "Server unreachable" });
//     }

//     setLoading(false);
//   };

//   const badgeColor = {
//     pending: "text-blue-400",
//     processing: "text-yellow-400",
//     waiting_generation: "text-purple-400",
//     completed: "text-green-400",
//     failed: "text-red-400"
//   };

//   return (
//     <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8">

//       <h2 className="text-2xl mb-6 text-yellow-400">Track Request</h2>

//       <input
//         placeholder="Enter Request ID"
//         value={rid}
//         onChange={(e)=>setRid(e.target.value)}
//         className="w-full p-3 mb-6 bg-black border border-zinc-700 rounded-lg"
//       />

//       <button
//         onClick={checkStatus}
//         disabled={loading}
//         className="w-full bg-yellow-600 hover:bg-yellow-500 py-3 rounded-lg disabled:opacity-50"
//       >
//         {loading ? "Checking..." : "Check Status"}
//       </button>

//       {status && !status.error && (
//         <div className="mt-8 text-center">

//           <p className="text-zinc-400">Status</p>
//           <p className={`text-xl mt-2 font-semibold ${badgeColor[status.status]}`}>
//             ● {status.status}
//           </p>

//           {status.status === "completed" && (
//             <p className="text-green-400 mt-4">
//               Dataset ready — go to Download page
//             </p>
//           )}

//           {status.status === "waiting_generation" && (
//             <p className="text-purple-400 mt-4">
//               Dataset will be generated soon
//             </p>
//           )}

//         </div>
//       )}

//       {status?.error && (
//         <div className="mt-6 text-red-400 text-center">
//           {status.error}
//         </div>
//       )}

//     </div>
//   );
// }
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API = import.meta.env.VITE_API_URL;

export default function TrackCard({ requestId: initialId = "", onReady }) {

  const [requestId, setRequestId] = useState(initialId);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const checkStatus = async () => {

    if (!requestId) return;

    setLoading(true);
    setStatus(null);

    try {
      const res = await fetch(`${API}/dataset/status/${requestId}`);
      const data = await res.json();

      if (!res.ok) {
        setStatus("not_found");
      } else {
        setStatus(data.status);
      }

    } catch {
      setStatus("error");
    }

    setLoading(false);
  };

  const goDownload = () => {
    // If used inside LandingPage staged flow
    if (onReady) onReady();

    // If used as standalone page
    navigate(`/download?rid=${requestId}`);
  };

  return (
    <div id="track" className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 text-center">

      <h2 className="text-2xl mb-6">Track Dataset</h2>

      {/* Manual input (important for returning users) */}
      <input
        value={requestId}
        onChange={(e) => setRequestId(e.target.value)}
        placeholder="Enter Request ID"
        className="w-full p-3 bg-black border border-zinc-700 rounded-lg mb-6"
      />

      <button
        onClick={checkStatus}
        disabled={loading}
        className="bg-yellow-600 px-6 py-3 rounded-lg disabled:opacity-50"
      >
        {loading ? "Checking..." : "Check Status"}
      </button>

      {/* STATUS DISPLAY */}
      {status && (
        <div className="mt-6">

          {status === "completed" && (
            <>
              <div className="text-lg font-semibold text-green-400">
                Dataset Ready ✓
              </div>

              <button
                onClick={goDownload}
                className="mt-6 bg-green-600 hover:bg-green-500 px-6 py-3 rounded-lg"
              >
                Go to Download
              </button>
            </>
          )}

          {status === "processing" && (
            <div className="text-yellow-400 text-lg font-semibold">
              Processing...
            </div>
          )}

          {status === "pending" && (
            <div className="text-yellow-400 text-lg font-semibold">
              Waiting in Queue...
            </div>
          )}

          {status === "waiting_generation" && (
            <div className="text-yellow-400 text-lg font-semibold">
              Generating Dataset...
            </div>
          )}

          {status === "not_found" && (
            <div className="text-red-400 text-lg font-semibold">
              Request ID not found
            </div>
          )}

          {status === "error" && (
            <div className="text-red-400 text-lg font-semibold">
              Server error
            </div>
          )}

        </div>
      )}

    </div>
  );
}

