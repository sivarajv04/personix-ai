import Section from "../../../shared/ui/Section";

const items = [
  {
    title: "AI Engineers",
    desc: "Train detection and recognition models without collecting real users"
  },
  {
    title: "Startups",
    desc: "Instant datasets without scraping, labeling or legal risk"
  },
  {
    title: "Researchers",
    desc: "Generate balanced demographic datasets for experiments"
  },
  {
    title: "Simulation Systems",
    desc: "Populate virtual environments with realistic humans"
  }
];

export default function TrustSection() {
  return (
    <Section
      title="Built For Real-World AI Development"
      subtitle="Personix AI replaces manual dataset collection with controllable synthetic data generation"
    >
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {items.map((item, i) => (
          <div
            key={i}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 hover:border-blue-500/40 transition"
          >
            <h3 className="text-lg font-medium mb-2">{item.title}</h3>
            <p className="text-zinc-400 text-sm">{item.desc}</p>
          </div>
        ))}
      </div>
    </Section>
  );
}
