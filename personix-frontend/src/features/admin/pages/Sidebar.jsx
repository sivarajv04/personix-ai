import { NavLink } from "react-router-dom";

const links = [
  { name: "Overview", path: "/admin/dashboard" },
  { name: "Instant Orders", path: "/admin/dashboard/orders" },
  { name: "Bulk Orders", path: "/admin/dashboard/bulk" },
  { name: "Inventory", path: "/admin/dashboard/inventory" },

  // ⭐ NEW PAGE
  { name: "System Monitor", path: "/admin/dashboard/system" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-zinc-950 border-r border-zinc-800 p-6">
      <h2 className="text-lg mb-6 text-white">Admin Panel</h2>

      <nav className="flex flex-col gap-2">
        {links.map(link => (
          <NavLink
            key={link.path}
            to={link.path}
            end={link.path === "/admin/dashboard"} // only exact match for overview
            className={({ isActive }) =>
              `px-4 py-2 rounded-lg transition ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
              }`
            }
          >
            {link.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

// import { NavLink } from "react-router-dom";

// export default function Sidebar() {

//   const link =
//     "block px-4 py-3 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition";

//   const active =
//     "bg-zinc-900 text-white";

//   return (
//     <aside className="w-64 min-h-screen border-r border-zinc-800 p-4">

//       <h2 className="text-lg mb-6 text-zinc-300">Admin Panel</h2>

//       <nav className="space-y-2">

//         <NavLink to="/admin/dashboard" className={({isActive}) => `${link} ${isActive ? active : ""}`}>
//           Overview
//         </NavLink>

//         <NavLink to="/admin/dashboard/orders" className={({isActive}) => `${link} ${isActive ? active : ""}`}>
//           Instant Orders
//         </NavLink>

//         <NavLink to="/admin/dashboard/bulk" className={({isActive}) => `${link} ${isActive ? active : ""}`}>
//           Bulk Orders
//         </NavLink>

//         <NavLink to="/admin/dashboard/inventory" className={({isActive}) => `${link} ${isActive ? active : ""}`}>
//           Inventory
//         </NavLink>

//       </nav>

//     </aside>
//   );
// }


// export default function Sidebar({ tab, setTab }) {

//   const item = (id, label) => (
//     <button
//       onClick={() => setTab(id)}
//       className={`w-full text-left px-4 py-3 rounded-lg mb-2 transition
//       ${tab === id ? "bg-zinc-800 text-white" : "text-zinc-400 hover:bg-zinc-900"}`}
//     >
//       {label}
//     </button>
//   );

//   return (
//     <div className="w-64 bg-zinc-950 border-r border-zinc-800 p-6">

//       <h2 className="text-xl mb-8 font-semibold">Admin Panel</h2>

//       {item("overview", "Overview")}
//       {item("instant", "Instant Orders")}
//       {item("bulk", "Bulk Orders")}
//       {item("inventory", "Inventory")}

//     </div>
//   );
// }
