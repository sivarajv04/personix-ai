import { useEffect, useState } from "react";
import { getInventory } from "../api/admin";

export default function Inventory() {

  const [items, setItems] = useState([]);

  useEffect(() => {
    getInventory().then(setItems).catch(console.error);
  }, []);

  function splitCategory(cat) {
    if (!cat) return ["-", "-"];
    const [gender, age] = cat.split("|").map(s => s.trim());
    return [gender, age];
  }

  return (
    <div>
      <h1 className="text-2xl mb-6">Generated Dataset Inventory</h1>

      <div className="border border-zinc-800 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-zinc-900 text-zinc-400">
            <tr>
              <th className="p-3 text-left">Gender</th>
              <th className="p-3 text-left">Age Bucket</th>
              <th className="p-3 text-left">Images Available</th>
            </tr>
          </thead>

          <tbody>
            {items.map((i, idx) => {
              const [gender, age] = splitCategory(i.category);

              return (
                <tr key={idx} className="border-t border-zinc-800">
                  <td className="p-3 capitalize">{gender}</td>
                  <td className="p-3">{age.replace("_", " - ")}</td>
                  <td className="p-3 font-semibold text-green-400">{i.images}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}


// import { useEffect, useState } from "react";
// import { getInventory } from "../api/admin";
// function formatDate(value) {
//   if (!value) return "-";

//   try {
//     // handles postgres date, timestamp, or ISO
//     const parsed =
//       typeof value === "string"
//         ? new Date(value.includes("T") ? value : value + "T00:00:00")
//         : new Date(value);

//     if (isNaN(parsed.getTime())) return "-";

//     return parsed.toLocaleString("en-IN", {
//       day: "2-digit",
//       month: "short",
//       year: "numeric",
//       hour: "2-digit",
//       minute: "2-digit"
//     });
//   } catch {
//     return "-";
//   }
// }


// export default function Inventory() {

//   const [items, setItems] = useState([]);

//   useEffect(() => {
//     getInventory().then(setItems).catch(console.error);
//   }, []);

//   return (
//     <div>
//       <h1 className="text-2xl mb-6">Generated Datasets</h1>

//       <div className="border border-zinc-800 rounded-xl overflow-hidden">
//         <table className="w-full text-sm">
//           <thead className="bg-zinc-900 text-zinc-400">
//             <tr>
//               <th className="p-3 text-left">Request ID</th>
//               <th className="p-3 text-left">Gender</th>
//               <th className="p-3 text-left">Age</th>
//               <th className="p-3 text-left">Count</th>
//               <th className="p-3 text-left">Created</th>
//             </tr>
//           </thead>

//           <tbody>
//             {items.map(i => (
//               <tr key={i.request_id} className="border-t border-zinc-800">
//                 <td className="p-3">{i.request_id}</td>
//                 <td className="p-3">{i.gender}</td>
//                 <td className="p-3">{i.age_bucket}</td>
//                 <td className="p-3">{i.count}</td>
//                 <td className="p-3">{new Date(i.created_at).toLocaleDateString()}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     </div>
//   );
// }
