import { useState } from "react";

const API = import.meta.env.VITE_API_URL;

export default function DownloadCard() {

  const [rid, setRid] = useState("");
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const download = async () => {

    if (!rid || !code) {
      setMessage("Enter request ID and passcode");
      return;
    }

    setLoading(true);
    setMessage("Preparing download...");

    try {
      const response = await fetch(
        `${API}/dataset/download/${rid}/${code}`,
        { method: "GET" }
      );

      // backend rejected
      if (!response.ok) {
        const text = await response.text();
        setMessage(text || "Invalid request ID or passcode");
        setLoading(false);
        return;
      }

      // read file
      const blob = await response.blob();

      // create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `dataset_${rid}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setMessage("Download started ✓");
    } catch {
      setMessage("Server unreachable");
    }

    setLoading(false);
  };

  return (
    <div id="download" className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 text-center">

      <h2 className="text-2xl mb-6 text-green-400">Download Dataset</h2>

      <input
        placeholder="Request ID"
        value={rid}
        onChange={(e)=>setRid(e.target.value)}
        className="w-full p-3 mb-4 bg-black rounded-lg border border-zinc-700"
      />

      <input
        placeholder="Passcode"
        value={code}
        onChange={(e)=>setCode(e.target.value)}
        className="w-full p-3 mb-6 bg-black rounded-lg border border-zinc-700"
      />

      <button
        onClick={download}
        disabled={loading}
        className="bg-green-600 hover:bg-green-500 px-8 py-3 rounded-lg text-lg disabled:opacity-50"
      >
        {loading ? "Downloading..." : "Download Dataset"}
      </button>

      {message && (
        <div className="mt-6 text-yellow-400">
          {message}
        </div>
      )}

    </div>
  );
}
