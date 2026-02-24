import Router from "./router";
import Header from "./shared/layout/Header";
import Footer from "./shared/layout/Footer";

export default function App() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col">

      <Header />

      <main className="flex-1">
        <Router />
      </main>

      <Footer />

    </div>
  );
}

// import Router from "./router";

// export default function App() {
//   return (
//     <div className="min-h-screen bg-black text-white">
//       <Router />
//     </div>
//   );
// }



// import Router from "./router";
// import Header from "./shared/layout/Header";

// export default function App() {
//   return (
//     <div className="bg-black min-h-screen text-white">
//       <Header />
//       <Router />
//     </div>
//   );
// }
