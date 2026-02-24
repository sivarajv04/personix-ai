import { Link, useLocation } from "react-router-dom";
import BackendStatus from "../components/BackendStatus";

export default function Header() {

  const { pathname } = useLocation();

  const nav = [
    { name: "Home", path: "/" },
    { name: "Request", path: "/request" },
    { name: "Track", path: "/track" },
    { name: "Download", path: "/download" },
    { name: "Bulk Order", path: "/bulk" },
    { name: "Admin", path: "/admin" },
  ];

  return (
    <header className="sticky top-0 z-50 bg-black/70 backdrop-blur border-b border-zinc-800">
    <div className="max-w-6xl mx-auto px-6 py-4 flex items-center">

        {/* LEFT — LOGO */}
        <Link to="/" className="text-xl font-bold tracking-wide text-white">
        Personix<span className="text-green-400">AI</span>
        </Link>

        {/* CENTER — FLEX SPACER */}
        <div className="flex-1" />

        {/* RIGHT — NAV + STATUS */}
        <div className="flex items-center gap-8">

        <nav className="flex gap-8 text-sm">
            {nav.map((item) => (
            <Link
                key={item.path}
                to={item.path}
                className={`transition ${
                pathname === item.path
                    ? "text-green-400"
                    : "text-zinc-400 hover:text-white"
                }`}
            >
                {item.name}
            </Link>
            ))}
        </nav>

        <BackendStatus />

        </div>
    </div>
    </header>

  );
}


// import { Link, useLocation } from "react-router-dom";
// import BackendStatus from "../components/BackendStatus";

// export default function Header() {

//   const { pathname } = useLocation();

//   const nav = [
//     { name: "Home", path: "/" },
//     { name: "Request", path: "/request" },
//     { name: "Track", path: "/track" },
//     { name: "Download", path: "/download" },
//     { name: "Bulk Order", path: "/bulk" },
//     { name: "Admin", path: "/admin" },
//   ];

//   return (
//     <header className="sticky top-0 z-50 bg-black/70 backdrop-blur border-b border-zinc-800">

//       <div className="max-w-6xl mx-auto px-6 py-4 flex items-center">

//         <Link to="/" className="text-xl font-bold tracking-wide text-white">
//             Personix<span className="text-green-400">AI</span>
//         </Link>

//         {/* Navigation */}
//         <nav className="flex gap-6 text-sm ml-12">
//             {nav.map((item) => (
//             <Link
//                 key={item.path}
//                 to={item.path}
//                 className={`transition ${
//                 pathname === item.path
//                     ? "text-green-400"
//                     : "text-zinc-400 hover:text-white"
//                 }`}
//             >
//                 {item.name}
//             </Link>
//             ))}
//         </nav>

//         {/* Status pushed to far right */}
//         <div className="ml-auto">
//             <BackendStatus />
//         </div>

//         </div>


//     </header>
//   );
// }
