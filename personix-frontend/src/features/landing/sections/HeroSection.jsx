import { Link } from "react-router-dom";

export default function HeroSection() {
  return (
    <section className="text-center py-28 border-b border-zinc-900">

      {/* TITLE */}
      <h1 className="text-5xl font-bold mb-6">
        PERSONIX AI
      </h1>

      {/* MAIN TAGLINE */}
      <p className="text-zinc-400 text-lg max-w-2xl mx-auto">
        Personix AI lets you create privacy-safe human datasets for AI training,
        testing and simulation — without collecting real user data or manual labeling.
      </p>

      {/* EXPLANATION */}
      <p className="text-zinc-500 max-w-2xl mx-auto mt-4 leading-relaxed">
        Instead of spending weeks gathering and cleaning data, generate structured
        datasets tailored to your requirements in minutes. Perfect for computer vision,
        ML experimentation, benchmarking and research environments.
      </p>

      {/* HOW IT WORKS */}
      <div className="mt-8 text-sm text-zinc-300 space-y-2">
        <p><span className="text-white font-medium">1.</span> Choose dataset type & attributes</p>
        <p><span className="text-white font-medium">2.</span> AI generates data in the background</p>
        <p><span className="text-white font-medium">3.</span> Track progress and download when ready</p>
      </div>

      {/* ACTION BUTTONS */}
      <div className="flex gap-6 justify-center mt-10">

        <Link
          to="/request"
          className="bg-blue-600 hover:bg-blue-500 px-8 py-4 rounded-xl font-semibold"
        >
          Generate Dataset
        </Link>

        <Link
          to="/track"
          className="bg-zinc-800 hover:bg-zinc-700 px-8 py-4 rounded-xl font-semibold"
        >
          Check Dataset Status
        </Link>

      </div>

      {/* FOOTNOTE */}
      <p className="text-sm text-zinc-500 mt-10">
        Used for AI training • Simulation • Testing • Privacy-safe research
      </p>

    </section>
  );
}