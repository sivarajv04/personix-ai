import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";

export default function Dashboard() {
  return (
    <div className="flex min-h-[calc(100vh-64px)]">

      <Sidebar />

      <div className="flex-1 p-8 bg-black">
        <Outlet />
      </div>

    </div>
  );
}


// import { Routes, Route, Navigate } from "react-router-dom";
// import Sidebar from "../components/Sidebar";
// import Overview from "../sections/Overview";

// import InstantOrders from "../sections/InstantOrders";
// import BulkOrders from "../sections/BulkOrders";
// import Inventory from "../sections/Inventory";

// export default function Dashboard() {
//   return (
//     <div className="flex min-h-[calc(100vh-64px)]">

//       {/* Sidebar */}
//       <Sidebar />

//       {/* Page Content */}
//       <div className="flex-1 p-8 bg-black">
//         <Routes>
//           <Route index element={<Overview />} />
//           <Route path="orders" element={<InstantOrders />} />
//           <Route path="bulk" element={<BulkOrders />} />
//           <Route path="inventory" element={<Inventory />} />
//           <Route path="*" element={<Navigate to="" replace />} />
//         </Routes>
//       </div>

//     </div>
//   );
// }
