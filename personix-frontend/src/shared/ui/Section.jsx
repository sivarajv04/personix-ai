export default function Section({ title, subtitle, children }) {
  return (
    <section className="py-24 border-b border-zinc-800">
      <div className="max-w-6xl mx-auto px-6">

        {(title || subtitle) && (
          <div className="text-center mb-16">
            {title && (
              <h2 className="text-4xl font-semibold mb-4">{title}</h2>
            )}
            {subtitle && (
              <p className="text-zinc-400 max-w-2xl mx-auto">{subtitle}</p>
            )}
          </div>
        )}

        {children}
      </div>
    </section>
  );
}
