export default function Features() {

  const features = [
    "Fully synthetic — zero privacy issues",
    "Structured metadata included",
    "CV-ready images",
    "Bulk dataset ordering",
    "Secure request-ID download system",
    "API integration ready"
  ];

  return (
    <section className="py-24 bg-zinc-950 border-y border-zinc-900">

      <h2 className="text-3xl font-semibold text-center mb-16">
        Features
      </h2>

      <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-6 px-6">
        {features.map((f,i)=>(
          <div key={i} className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
            {f}
          </div>
        ))}
      </div>

    </section>
  );
}
