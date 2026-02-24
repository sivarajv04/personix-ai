export default function ApiSection() {
  return (
    <section className="border-t border-zinc-800 py-24">
      <div className="max-w-5xl mx-auto px-6 text-center">

        <h2 className="text-3xl font-semibold mb-4">Simple API Integration</h2>
        <p className="text-zinc-400 mb-12 max-w-2xl mx-auto">
          Personix AI can be integrated directly into ML pipelines, backend services,
          and automated dataset workflows using simple REST endpoints.
        </p>

        <div className="bg-black border border-zinc-700 rounded-2xl p-8 text-left overflow-x-auto">
<pre className="text-green-400 text-sm">
{`POST /dataset/request
{
  "gender": "male",
  "age_bucket": "26_40",
  "count": 100
}

GET /dataset/status/{request_id}

GET /dataset/download/{request_id}/{auth_code}`}
</pre>
        </div>

        <p className="text-zinc-500 mt-6 text-sm">
          Works with Python, Node.js, automation pipelines and training scripts
        </p>

      </div>
    </section>
  );
}
