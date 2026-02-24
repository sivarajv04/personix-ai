export default function Section({ id, title, children }) {
  return (
    <section id={id} className="py-24 border-b border-zinc-900">
      <div className="max-w-5xl mx-auto px-6">
        {title && (
          <h2 className="text-3xl font-semibold mb-10">
            {title}
          </h2>
        )}
        {children}
      </div>
    </section>
  );
}
