import { Navigate, Outlet, useLocation } from "react-router-dom";

export default function AdminRoute() {
  const token = localStorage.getItem("personix_admin_token");
  const location = useLocation();

  // allow login page
  if (!token && location.pathname === "/admin") {
    return <Outlet />;
  }

  // block dashboard
  if (!token) {
    return <Navigate to="/admin" replace />;
  }

  return <Outlet />;
}
// import { Navigate } from "react-router-dom";

// export default function AdminRoute({ children }) {
//   const token = localStorage.getItem("personix_admin_token");

//   if (!token) {
//     return <Navigate to="/admin" replace />;
//   }

//   return children;
// }


// import { Navigate } from "react-router-dom";

// export default function AdminRoute({ children }) {

//   const token = localStorage.getItem("personix_admin_token");

//   if (!token) {
//     return <Navigate to="/admin" replace />;
//   }

//   return children;
// }


// import { Navigate } from "react-router-dom";

// export default function AdminRoute({ children }) {

//   const isAdmin = localStorage.getItem("personix_admin") === "true";

//   if (!isAdmin) {
//     return <Navigate to="/admin" replace />;
//   }

//   return children;
// }

