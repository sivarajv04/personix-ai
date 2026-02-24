import { Link } from "react-router-dom";
// import Footer from "../../../shared/layout/Footer";
import HeroSection from "../sections/HeroSection";
import TrustSection from "../sections/TrustSection";
import ProblemSolution from "../sections/ProblemSolution";
import ApiSection from "../sections/ApiSection";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <HeroSection />
      {/* HERO
      <section className="text-center pt-32 pb-24 border-b border-zinc-800">
        <h1 className="text-5xl font-bold mb-4">Personix AI</h1>
        <p className="text-zinc-400 max-w-xl mx-auto">
          Generate structured synthetic human datasets for AI training,
          testing, and simulation environments — on demand.
        </p>

        <div className="mt-8 flex gap-4 justify-center">
          <Link to="/request" className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-xl">
            Create Dataset
          </Link>
          <Link to="/track" className="bg-zinc-800 hover:bg-zinc-700 px-6 py-3 rounded-xl">
            Track Order
          </Link>
        </div>
      </section>
    <TrustSection />
    <ProblemSolution />
    <ApiSection /> */}


      {/* HOW IT WORKS */}
      <section className="max-w-5xl mx-auto px-6 py-24">
        <h2 className="text-3xl font-semibold mb-12 text-center">How It Works</h2>

        <div className="grid md:grid-cols-4 gap-8 text-center">
          <Step number="1" title="Create Order" desc="Select dataset parameters" />
          <Step number="2" title="Processing" desc="AI generates dataset" />
          <Step number="3" title="Track Status" desc="Monitor generation" />
          <Step number="4" title="Download" desc="Secure download with passcode" />
        </div>
      </section>


      {/* FEATURES */}
      <section className="border-t border-zinc-800 py-24">
        <div className="max-w-5xl mx-auto px-6 grid md:grid-cols-3 gap-10 text-center">
          <Feature title="API Ready" desc="Integrate dataset generation into your pipelines" />
          <Feature title="Secure Access" desc="Every dataset protected by request ID + passcode" />
          <Feature title="Scalable" desc="Supports multiple simultaneous customers safely" />
        </div>
      </section>


      {/* TRY IT NOW */}
      <section className="text-center py-24 border-t border-zinc-800">
        <h2 className="text-3xl mb-6">Try Personix</h2>

        <div className="flex justify-center gap-6">
          <Link to="/request" className="bg-blue-600 px-8 py-3 rounded-xl">
            Request Dataset
          </Link>

          <Link to="/download" className="bg-green-600 px-8 py-3 rounded-xl">
            Download Dataset
          </Link>
        </div>
      </section>

      {/* <Footer /> */}
    </main>
  );
}


/* ---------- Small Components ---------- */

function Step({ number, title, desc }) {
  return (
    <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800">
      <div className="text-blue-400 text-xl font-bold mb-2">{number}</div>
      <div className="font-semibold">{title}</div>
      <div className="text-sm text-zinc-400 mt-1">{desc}</div>
    </div>
  );
}

function Feature({ title, desc }) {
  return (
    <div className="p-8 bg-zinc-900 rounded-2xl border border-zinc-800">
      <div className="text-xl font-semibold mb-3">{title}</div>
      <p className="text-zinc-400">{desc}</p>
    </div>
  );
}



// import { useState } from "react";
// import RequestCard from "../tools/RequestCard";
// import TrackCard from "../tools/TrackCard";
// import DownloadCard from "../tools/DownloadCard";

// export default function LandingPage() {

//   const [stage, setStage] = useState("request");
//   const [requestId, setRequestId] = useState("");
//   const [passcode, setPasscode] = useState("");

//   return (
//     <main className="min-h-screen bg-black text-white">

//       {/* HERO */}
//       <section className="text-center pt-28 pb-12 border-b border-zinc-800">
//         <h1 className="text-5xl font-bold mb-3">Personix AI</h1>
//         <p className="text-zinc-400">
//           Generate and download structured synthetic human datasets
//         </p>
//       </section>

//       <section className="max-w-4xl mx-auto px-6 py-16">

//         {stage === "request" && (
//           <RequestCard
//             onCreated={(rid, code) => {
//               setRequestId(rid);
//               setPasscode(code);
//               setStage("track");
//             }}
//           />
//         )}

//         {stage === "track" && (
//           <TrackCard
//             requestId={requestId}
//             onReady={() => setStage("download")}
//           />
//         )}

//         {stage === "download" && (
//           <DownloadCard
//             requestId={requestId}
//             passcode={passcode}
//           />
//         )}

//       </section>

//     </main>
//   );
// }
