import TrackCard from "../../landing/tools/TrackCard";

export default function TrackPage() {
  return (
    <main className="max-w-3xl mx-auto px-6 py-24">
      <TrackCard />
    </main>
  );
}

// import { useState } from "react";
// import TrackCard from "../../landing/tools/TrackCard.jsx";


// export default function TrackPage() {

//   const [rid, setRid] = useState("");

//   return (
//     <main className="max-w-3xl mx-auto px-6 py-24">

//       <h1 className="text-4xl font-bold mb-10">Track Dataset</h1>

//       <input
//         placeholder="Enter Request ID"
//         value={rid}
//         onChange={(e)=>setRid(e.target.value)}
//         className="w-full p-3 mb-8 bg-black border border-zinc-700 rounded-lg"
//       />

//       <TrackCard requestId={rid} />

//     </main>
//   );
// }
