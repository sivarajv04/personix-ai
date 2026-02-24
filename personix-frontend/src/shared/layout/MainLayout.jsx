import Header from "../shared/layout/Header";
import { Outlet } from "react-router-dom";

export default function MainLayout() {
  return (
    <div className="bg-black text-white min-h-screen">
      <Header />
      <Outlet />
    </div>
  );
}
