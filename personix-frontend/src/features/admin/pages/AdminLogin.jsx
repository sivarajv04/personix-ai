import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API = import.meta.env.VITE_API_URL;

export default function AdminLogin() {

  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const login = async () => {
    setError("");

    try {
      const res = await fetch(`${API}/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
      });

      if (!res.ok) {
        setError("Wrong password");
        return;
      }

      const data = await res.json();

      // store admin session token
      localStorage.setItem("personix_admin_token", data.token || "true");

      navigate("/admin/dashboard", { replace: true });

    } catch {
      setError("Server not reachable");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">

      {/* FORM WRAPPER */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          login();
        }}
        className="bg-zinc-900 border border-zinc-800 rounded-2xl p-10 w-96"
      >

        <h1 className="text-2xl mb-6 text-center">Admin Access</h1>

        <input
          type="password"
          placeholder="Enter admin password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg mb-4"
        />

        {error && (
          <p className="text-red-400 text-sm mb-3">{error}</p>
        )}

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-lg"
        >
          Login
        </button>

      </form>
    </div>
  );
}


// import { useState } from "react";
// import { useNavigate } from "react-router-dom";

// const API = "http://127.0.0.1:8000";

// export default function AdminLogin() {

//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");
//   const navigate = useNavigate();

//   const login = async () => {
//     setError("");

//     try {
//       const res = await fetch(`${API}/admin/login`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ password })
//       });

//       if (!res.ok) throw new Error();

//       const data = await res.json();

//       localStorage.setItem("admin_token", data.token);

//       navigate("/admin/dashboard");

//     } catch {
//       setError("Invalid password");
//     }
//   };

//   return (
//     <div className="min-h-screen bg-black text-white flex items-center justify-center">

//       <div className="bg-zinc-900 p-10 rounded-2xl border border-zinc-800 w-96">

//         <h1 className="text-2xl mb-6 text-center">Admin Access</h1>

//         <input
//           type="password"
//           placeholder="Enter admin password"
//           value={password}
//           onChange={e=>setPassword(e.target.value)}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg mb-4"
//         />

//         <button
//           onClick={login}
//           className="w-full bg-blue-600 py-3 rounded-lg hover:bg-blue-500"
//         >
//           Login
//         </button>

//         {error && (
//           <p className="text-red-400 mt-4 text-center">{error}</p>
//         )}

//       </div>
//     </div>
//   );
// }
