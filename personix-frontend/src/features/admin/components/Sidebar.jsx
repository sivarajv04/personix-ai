import { NavLink } from "react-router-dom";

const links = [
  { name: "Overview", path: "/admin/dashboard" },
  { name: "Instant Orders", path: "/admin/dashboard/orders" },
  { name: "Bulk Orders", path: "/admin/dashboard/bulk" },
  { name: "Inventory", path: "/admin/dashboard/inventory" },

  // ⭐ System Monitor
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
            end={link.path === "/admin/dashboard"}
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
//     "block px-4 py-3 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900";
//   const active =
//     "block px-4 py-3 rounded-lg text-white bg-zinc-900";

//   return (
//     <div className="w-64 border-r border-zinc-800 p-4 space-y-2">

//       <NavLink to="" end className={({isActive}) => isActive ? active : link}>
//         Overview
//       </NavLink>

//       <NavLink to="orders" className={({isActive}) => isActive ? active : link}>
//         Instant Orders
//       </NavLink>

//       <NavLink to="bulk" className={({isActive}) => isActive ? active : link}>
//         Bulk Orders
//       </NavLink>

//       <NavLink to="inventory" className={({isActive}) => isActive ? active : link}>
//         Inventory
//       </NavLink>

//     </div>
//   );
// }
