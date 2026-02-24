import os
import shutil

ROOT = "src"

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ---------- reset ----------
if os.path.exists(ROOT):
    print("Deleting existing src folder...")
    shutil.rmtree(ROOT)

print("Creating fresh frontend structure...\n")

files = {

# ---------------- core ----------------
"src/main.jsx": """
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./styles/global.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",

"src/App.jsx": """
import AppRouter from "./app/router";
function App() {
  return <AppRouter />;
}
export default App;
""",

# ---------------- router ----------------
"src/app/router.jsx": """
import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingPage from "../features/landing/pages/LandingPage.jsx";
import RequestPage from "../features/request/pages/RequestPage.jsx";
import TrackPage from "../features/track/pages/TrackPage.jsx";
import DownloadPage from "../features/download/pages/DownloadPage.jsx";
import AdminDashboard from "../features/admin/pages/AdminDashboard.jsx";

import MainLayout from "../layouts/MainLayout.jsx";
import PortalLayout from "../layouts/PortalLayout.jsx";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        <Route element={<MainLayout />}>
          <Route path="/" element={<LandingPage />} />
        </Route>

        <Route element={<PortalLayout />}>
          <Route path="/request" element={<RequestPage />} />
          <Route path="/track" element={<TrackPage />} />
          <Route path="/download" element={<DownloadPage />} />
        </Route>

        <Route path="/admin" element={<AdminDashboard />} />

      </Routes>
    </BrowserRouter>
  );
}
""",

# ---------------- layouts ----------------
"src/layouts/MainLayout.jsx": """
import { Outlet } from "react-router-dom";
import Navbar from "../shared/ui/Navbar";

export default function MainLayout() {
  return (
    <div className="bg-black min-h-screen text-white">
      <Navbar />
      <Outlet />
    </div>
  );
}
""",

"src/layouts/PortalLayout.jsx": """
import { Outlet } from "react-router-dom";

export default function PortalLayout() {
  return (
    <div className="bg-black min-h-screen text-white">
      <h2 className="p-4 border-b border-zinc-800">Client Portal</h2>
      <Outlet />
    </div>
  );
}
""",

# ---------------- shared UI ----------------
"src/shared/ui/Navbar.jsx": """
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="border-b border-zinc-800 bg-black text-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">

        <Link to="/" className="text-xl font-bold tracking-wide">
          Personix AI
        </Link>

        <div className="flex gap-6 text-sm text-zinc-300">
          <Link to="/">Home</Link>
          <Link to="/request">Portal</Link>
          <Link to="/admin">Admin</Link>
        </div>

      </div>
    </nav>
  );
}
""",

"src/shared/ui/Container.jsx": """
export default function Container({ children }) {
  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      {children}
    </div>
  );
}
""",

"src/shared/ui/Button.jsx": """
export default function Button({ children, onClick }) {
  return (
    <button
      onClick={onClick}
      className="bg-white text-black px-5 py-2 rounded-lg font-medium hover:bg-zinc-200 transition"
    >
      {children}
    </button>
  );
}
""",

# ---------------- landing ----------------
"src/features/landing/pages/LandingPage.jsx": """
import { useNavigate } from "react-router-dom";
import Container from "../../../shared/ui/Container";
import Button from "../../../shared/ui/Button";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <Container>

      <div className="text-center py-24">
        <h1 className="text-5xl font-bold mb-6">
          Synthetic Human Dataset API
        </h1>

        <p className="text-zinc-400 text-lg mb-10 max-w-2xl mx-auto">
          Request structured AI-ready human datasets instantly.
          Track generation status and download securely using a request ID.
        </p>

        <Button onClick={() => navigate("/request")}>
          Request Dataset
        </Button>
      </div>

      <div className="grid md:grid-cols-3 gap-10 py-20 text-center">
        <div>
          <h3 className="text-xl font-semibold mb-3">Structured Data</h3>
          <p className="text-zinc-400">Choose gender, age bucket and sample count.</p>
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-3">Secure Download</h3>
          <p className="text-zinc-400">Access datasets using request ID and passcode only.</p>
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-3">Generation Engine</h3>
          <p className="text-zinc-400">Automatic generation when stock is unavailable.</p>
        </div>
      </div>

    </Container>
  );
}
""",

# ---------------- placeholder pages ----------------
"src/features/request/pages/RequestPage.jsx": """export default function RequestPage(){ return <div className='p-10'>Request Page</div>}""",
"src/features/track/pages/TrackPage.jsx": """export default function TrackPage(){ return <div className='p-10'>Track Page</div>}""",
"src/features/download/pages/DownloadPage.jsx": """export default function DownloadPage(){ return <div className='p-10'>Download Page</div>}""",
"src/features/admin/pages/AdminDashboard.jsx": """export default function AdminDashboard(){ return <div className='p-10'>Admin Dashboard</div>}""",

# ---------------- styles ----------------
"src/styles/global.css": """
body {
  margin: 0;
  font-family: Inter, system-ui, Arial;
  background: black;
  color: white;
}
"""
}

# ---------- create ----------
for path, content in files.items():
    write(path, content)
    print("Created:", path)

print("\\nFrontend base ready ✅")


# import os
# import shutil

# ROOT = "src"

# # ---------- helper ----------
# def write(path, content):
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     with open(path, "w", encoding="utf-8") as f:
#         f.write(content.strip() + "\n")


# # ---------- reset ----------
# if os.path.exists(ROOT):
#     print("Deleting existing src folder...")
#     shutil.rmtree(ROOT)

# print("Creating fresh frontend structure...\n")

# # ---------- files ----------
# files = {

# "src/main.jsx": """
# import React from "react";
# import ReactDOM from "react-dom/client";
# import App from "./App.jsx";

# ReactDOM.createRoot(document.getElementById("root")).render(
#   <React.StrictMode>
#     <App />
#   </React.StrictMode>
# );
# """,

# "src/App.jsx": """
# import AppRouter from "./app/router";

# function App() {
#   return <AppRouter />;
# }

# export default App;
# """,

# "src/app/router.jsx": """
# import { BrowserRouter, Routes, Route } from "react-router-dom";

# import LandingPage from "../features/landing/pages/LandingPage.jsx";
# import RequestPage from "../features/request/pages/RequestPage.jsx";
# import TrackPage from "../features/track/pages/TrackPage.jsx";
# import DownloadPage from "../features/download/pages/DownloadPage.jsx";
# import AdminDashboard from "../features/admin/pages/AdminDashboard.jsx";

# import MainLayout from "../layouts/MainLayout.jsx";
# import PortalLayout from "../layouts/PortalLayout.jsx";

# function AppRouter() {
#   return (
#     <BrowserRouter>
#       <Routes>

#         <Route element={<MainLayout />}>
#           <Route path="/" element={<LandingPage />} />
#         </Route>

#         <Route element={<PortalLayout />}>
#           <Route path="/request" element={<RequestPage />} />
#           <Route path="/track" element={<TrackPage />} />
#           <Route path="/download" element={<DownloadPage />} />
#         </Route>

#         <Route path="/admin" element={<AdminDashboard />} />

#       </Routes>
#     </BrowserRouter>
#   );
# }

# export default AppRouter;
# """,

# "src/layouts/MainLayout.jsx": """
# import { Outlet } from "react-router-dom";

# export default function MainLayout() {
#   return (
#     <div>
#       <h2>Main Layout</h2>
#       <Outlet />
#     </div>
#   );
# }
# """,

# "src/layouts/PortalLayout.jsx": """
# import { Outlet } from "react-router-dom";

# export default function PortalLayout() {
#   return (
#     <div>
#       <h2>Portal Layout</h2>
#       <Outlet />
#     </div>
#   );
# }
# """,

# "src/features/landing/pages/LandingPage.jsx": """
# export default function LandingPage() {
#   return <div>Landing Page</div>;
# }
# """,

# "src/features/request/pages/RequestPage.jsx": """
# export default function RequestPage() {
#   return <div>Request Page</div>;
# }
# """,

# "src/features/track/pages/TrackPage.jsx": """
# export default function TrackPage() {
#   return <div>Track Page</div>;
# }
# """,

# "src/features/download/pages/DownloadPage.jsx": """
# export default function DownloadPage() {
#   return <div>Download Page</div>;
# }
# """,

# "src/features/admin/pages/AdminDashboard.jsx": """
# export default function AdminDashboard() {
#   return <div>Admin Dashboard</div>;
# }
# """,
# }

# # ---------- create ----------
# for path, content in files.items():
#     write(path, content)
#     print("Created:", path)

# print("\nFrontend structure ready ✅")
