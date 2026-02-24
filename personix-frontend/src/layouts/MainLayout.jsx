import Header from "../shared/layout/Header";

export default function MainLayout({ children }) {
  return (
    <div className="bg-black text-white min-h-screen">
      <Header />
      {children}
    </div>
  );
}
