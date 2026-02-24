export default function HowItWorks() {
  const steps = [
    ["1. Request", "Choose attributes and create dataset order"],
    ["2. Generate", "Our engine synthesizes human images"],
    ["3. Verify", "Track order status using request ID"],
    ["4. Download", "Secure download using passcode"],
  ];

  return (
    <section className="py-24 max-w-5xl mx-auto px-6">

      <h2 className="text-3xl font-semibold text-center mb-16">
        How it works
      </h2>

      <div className="grid md:grid-cols-4 gap-8">
        {steps.map(([title, desc], i) => (
          <div key={i} className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 text-center">
            <div className="text-blue-400 font-semibold mb-3">{title}</div>
            <div className="text-zinc-400 text-sm">{desc}</div>
          </div>
        ))}
      </div>

    </section>
  );
}
