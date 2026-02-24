export default function StatCard({ title, value }) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-5">
      <p className="text-zinc-400 text-sm">{title}</p>
      <p className="text-3xl mt-2 font-semibold">{value ?? "--"}</p>
    </div>
  );
}
