import { Routes, Route } from "react-router-dom";

import LandingPage from "./features/landing/pages/LandingPage.jsx";
import RequestPage from "./features/tools/pages/RequestPage.jsx";
import TrackPage from "./features/tools/pages/TrackPage.jsx";
import DownloadPage from "./features/tools/pages/DownloadPage.jsx";
import BulkPage from "./features/bulk/pages/BulkPage.jsx";

import AdminLogin from "./features/admin/pages/AdminLogin.jsx";
import Dashboard from "./features/admin/pages/Dashboard.jsx";
import AdminRoute from "./shared/auth/AdminRoute.jsx";

import Overview from "./features/admin/sections/Overview.jsx";
import InstantOrders from "./features/admin/sections/InstantOrders.jsx";
import BulkOrders from "./features/admin/sections/BulkOrders.jsx";
import Inventory from "./features/admin/sections/Inventory.jsx";
import SystemMonitor from "./features/admin/sections/SystemMonitor.jsx";
export default function Router() {
  return (
    <Routes>

      {/* PUBLIC */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/request" element={<RequestPage />} />
      <Route path="/track" element={<TrackPage />} />
      <Route path="/download" element={<DownloadPage />} />
      <Route path="/bulk" element={<BulkPage />} />

      {/* ADMIN LOGIN */}
      <Route path="/admin" element={<AdminLogin />} />

      {/* ADMIN AREA */}
      <Route path="/admin" element={<AdminRoute />}>
        <Route index element={<AdminLogin />} />

        <Route path="dashboard" element={<Dashboard />}>
          <Route index element={<Overview />} />
          <Route path="orders" element={<InstantOrders />} />
          <Route path="bulk" element={<BulkOrders />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="system" element={<SystemMonitor />} />
        </Route>
      </Route>

    </Routes>
  );
}


// import { Routes, Route } from "react-router-dom";

// import LandingPage from "./features/landing/pages/LandingPage.jsx";
// import RequestPage from "./features/tools/pages/RequestPage.jsx";
// import TrackPage from "./features/tools/pages/TrackPage.jsx";
// import DownloadPage from "./features/tools/pages/DownloadPage.jsx";
// import BulkPage from "./features/bulk/pages/BulkPage.jsx";
// import AdminLogin from "./features/admin/pages/AdminLogin.jsx";
// import Dashboard from "./features/admin/pages/Dashboard.jsx";
// import AdminRoute from "./shared/auth/AdminRoute.jsx";

// export default function Router() {
//   return (
//     <Routes>

//       {/* Public */}
//       <Route path="/" element={<LandingPage />} />
//       <Route path="/request" element={<RequestPage />} />
//       <Route path="/track" element={<TrackPage />} />
//       <Route path="/download" element={<DownloadPage />} />
//       <Route path="/bulk" element={<BulkPage />} />

//       {/* Admin */}
//       <Route path="/admin" element={<AdminLogin />} />

//       <Route
//         path="/admin/dashboard/*"
//         element={
//           <AdminRoute>
//             <Dashboard />
//           </AdminRoute>
//         }
//       />

//     </Routes>
//   );
// }


// import { Routes, Route } from "react-router-dom";

// import LandingPage from "./features/landing/pages/LandingPage.jsx";
// import RequestPage from "./features/tools/pages/RequestPage.jsx";
// import TrackPage from "./features/tools/pages/TrackPage.jsx";
// import DownloadPage from "./features/tools/pages/DownloadPage.jsx";
// import BulkPage from "./features/bulk/pages/BulkPage.jsx";
// import AdminLogin from "./features/admin/pages/AdminLogin.jsx";
// import Dashboard from "./features/admin/pages/Dashboard.jsx";
// import AdminRoute from "./shared/auth/AdminRoute.jsx";

// export default function Router() {
//   return (
//     <Routes>
//       <Route path="/" element={<LandingPage />} />
//       <Route path="/request" element={<RequestPage />} />
//       <Route path="/track" element={<TrackPage />} />
//       <Route path="/download" element={<DownloadPage />} />
//       <Route path="/bulk" element={<BulkPage />} />
//       <Route path="/admin" element={<AdminLogin />}>
//         <Route path="dashboard" element={<AdminRoute><Dashboard /></AdminRoute>} />
//       </Route>
//       <Route path="/admin" element={<AdminLogin />} />
//       <Route
//         path="/admin/dashboard"
//         element={
//             <AdminRoute>
//             <Dashboard />
//             </AdminRoute>
//         }
//         />
//        </Routes>
//   );
// }
