import { useState } from "react";

const API = import.meta.env.VITE_API_URL;

export default function RequestCard() {

  const [gender, setGender] = useState("male");
  const [age, setAge] = useState("26_40");
  const [count, setCount] = useState(1);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState("");

  const createOrder = async () => {

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API}/dataset/request`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          gender,
          age_bucket: age,
          count: Number(count),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setResult({ error: data.detail || "Failed to create order" });
        setLoading(false);
        return;
      }

      // safer passcode extraction
      const passcode =
        data.passcode ??
        data.message?.match(/\d+/)?.[0] ??
        "";

      setResult({
        request_id: data.request_id,
        passcode: passcode,
      });

    } catch {
      setResult({ error: "Server unreachable" });
    }

    setLoading(false);
  };

  const copy = (text, type) => {
    navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(""), 1500);
  };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8">

      <h2 className="text-2xl mb-6 text-blue-400">Request Dataset</h2>

      {/* FORM */}
      <div className="space-y-4">

        <select
          value={gender}
          onChange={(e)=>setGender(e.target.value)}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
        >
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>

        <select
          value={age}
          onChange={(e)=>setAge(e.target.value)}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
        >
          <option value="0_18">0-18</option>
          <option value="18_25">18-25</option>
          <option value="26_40">26-40</option>
          <option value="40_60">40-60</option>
          <option value="60_plus">60+</option>
        </select>

        <input
          type="number"
          min="1"
          value={count}
          onChange={(e)=>setCount(e.target.value)}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
          placeholder="Number of images"
        />

        <button
          onClick={createOrder}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-lg disabled:opacity-50"
        >
          {loading ? "Creating..." : "Create Order"}
        </button>

      </div>

      {/* RESULT */}
      {result && !result.error && (
        <div className="mt-8 bg-black border border-zinc-700 rounded-lg p-5 text-sm space-y-4">

          <div className="text-green-400 font-medium">
            Order created successfully ✓
          </div>

          <div>
            <span className="text-zinc-400">Request ID:</span>
            <div className="flex justify-between items-center mt-1">
              <span className="text-green-400">{result.request_id}</span>
              <button
                onClick={()=>copy(result.request_id, "id")}
                className="text-xs text-zinc-400 hover:text-white"
              >
                {copied === "id" ? "Copied ✓" : "Copy"}
              </button>
            </div>
          </div>

          <div>
            <span className="text-zinc-400">Passcode:</span>
            <div className="flex justify-between items-center mt-1">
              <span className="text-yellow-400">{result.passcode}</span>
              <button
                onClick={()=>copy(result.passcode, "code")}
                className="text-xs text-zinc-400 hover:text-white"
              >
                {copied === "code" ? "Copied ✓" : "Copy"}
              </button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-3">
            <a
              href="/track"
              className="flex-1 text-center bg-yellow-600 hover:bg-yellow-500 py-2 rounded-lg text-sm"
            >
              Track Order
            </a>

            <a
              href="/download"
              className="flex-1 text-center bg-green-600 hover:bg-green-500 py-2 rounded-lg text-sm"
            >
              Download Page
            </a>
          </div>

        </div>
      )}

      {result?.error && (
        <div className="mt-6 text-red-400">
          {result.error}
        </div>
      )}

    </div>
  );
}



// import { useState } from "react";

// const API = "http://127.0.0.1:8000";

// export default function RequestCard({ onCreated }) {

//   const [gender, setGender] = useState("male");
//   const [age, setAge] = useState("26_40");
//   const [count, setCount] = useState(1);

//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [copied, setCopied] = useState("");

//   const createOrder = async () => {

//     setLoading(true);
//     setResult(null);

//     try {
//       const res = await fetch(`${API}/dataset/request`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           gender,
//           age_bucket: age,
//           count: Number(count),
//         }),
//       });

//       const data = await res.json();

//       if (!res.ok) {
//         setResult({ error: data.detail || "Failed to create order" });
//         setLoading(false);
//         return;
//       }

//       // extract passcode from message
//       const passcode = data.message.match(/\d+/)?.[0];

//       setResult({
//         request_id: data.request_id,
//         passcode: passcode,
//       });

//       if (onCreated) onCreated(data.request_id, passcode);

//     } catch {
//       setResult({ error: "Server unreachable" });
//     }

//     setLoading(false);
//   };

//   const copy = (text, type) => {
//     navigator.clipboard.writeText(text);
//     setCopied(type);
//     setTimeout(() => setCopied(""), 1500);
//   };

//   return (
//     <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8">

//       <h2 className="text-2xl mb-6 text-blue-400">Request Dataset</h2>

//       {/* FORM */}
//       <div className="space-y-4">

//         <select
//           value={gender}
//           onChange={(e)=>setGender(e.target.value)}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//         >
//           <option value="male">Male</option>
//           <option value="female">Female</option>
//         </select>

//         <select
//           value={age}
//           onChange={(e)=>setAge(e.target.value)}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//         >
//           <option value="0_18">0-18</option>
//           <option value="18_25">18-25</option>
//           <option value="26_40">26-40</option>
//           <option value="40_60">40-60</option>
//           <option value="60_plus">60+</option>
//         </select>

//         <input
//           type="number"
//           min="1"
//           value={count}
//           onChange={(e)=>setCount(e.target.value)}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//           placeholder="Number of images"
//         />

//         <button
//           onClick={createOrder}
//           disabled={loading}
//           className="w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-lg disabled:opacity-50"
//         >
//           {loading ? "Creating..." : "Create Order"}
//         </button>

//       </div>

//       {/* RESULT */}
//       {result && !result.error && (
//         <div className="mt-8 bg-black border border-zinc-700 rounded-lg p-4 text-sm space-y-3">

//           <div>
//             <span className="text-zinc-400">Request ID:</span>
//             <div className="flex justify-between items-center mt-1">
//               <span className="text-green-400">{result.request_id}</span>
//               <button
//                 onClick={()=>copy(result.request_id, "id")}
//                 className="text-xs text-zinc-400 hover:text-white"
//               >
//                 {copied === "id" ? "Copied ✓" : "Copy"}
//               </button>
//             </div>
//           </div>

//           <div>
//             <span className="text-zinc-400">Passcode:</span>
//             <div className="flex justify-between items-center mt-1">
//               <span className="text-yellow-400">{result.passcode}</span>
//               <button
//                 onClick={()=>copy(result.passcode, "code")}
//                 className="text-xs text-zinc-400 hover:text-white"
//               >
//                 {copied === "code" ? "Copied ✓" : "Copy"}
//               </button>
//             </div>
//           </div>

//         </div>
//       )}

//       {result?.error && (
//         <div className="mt-6 text-red-400">
//           {result.error}
//         </div>
//       )}

//     </div>
//   );
// }

