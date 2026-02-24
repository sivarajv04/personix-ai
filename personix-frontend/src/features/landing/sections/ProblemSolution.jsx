import Section from "../../../shared/ui/Section";

export default function ProblemSolution() {
  return (
    <Section
      title="Why Synthetic Human Data?"
      subtitle="Collecting real human datasets is expensive, risky and slow. Personix removes the entire bottleneck."
    >
      <div className="grid md:grid-cols-2 gap-10">

        {/* Problem */}
        <div className="bg-red-950/20 border border-red-900/40 rounded-2xl p-8">
          <h3 className="text-2xl mb-4 text-red-400">The Traditional Way</h3>
          <ul className="space-y-3 text-zinc-300 text-sm">
            <li>Privacy & consent management</li>
            <li>Legal compliance risk (GDPR / biometric laws)</li>
            <li>Manual data collection & annotation</li>
            <li>Biased or unbalanced datasets</li>
            <li>Expensive human labeling</li>
          </ul>
        </div>

        {/* Solution */}
        <div className="bg-green-950/20 border border-green-900/40 rounded-2xl p-8">
          <h3 className="text-2xl mb-4 text-green-400">The Personix Way</h3>
          <ul className="space-y-3 text-zinc-300 text-sm">
            <li>Instant synthetic generation</li>
            <li>No real identities stored</li>
            <li>Balanced demographics</li>
            <li>Fully automated pipeline</li>
            <li>Ready for ML training</li>
          </ul>
        </div>

      </div>
    </Section>
  );
}
