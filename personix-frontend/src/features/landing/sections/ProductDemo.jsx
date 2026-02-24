import RequestCard from "../../tools/RequestCard";
import { Link } from "react-router-dom";

export default function ProductDemo() {
  return (
    <section className="py-28 border-t border-zinc-900">

      <h2 className="text-3xl font-semibold text-center mb-6">
        Try It Now
      </h2>

      <p className="text-center text-zinc-400 mb-16">
        Create a synthetic dataset instantly — no signup required
      </p>

      <div className="max-w-2xl mx-auto px-6">
        <RequestCard />
      </div>

      <div className="text-center mt-12 text-sm text-zinc-500">
        Already ordered?{" "}
        <Link to="/track" className="text-blue-400 hover:underline">
          Track your request
        </Link>
        {" "}•{" "}
        <Link to="/download" className="text-green-400 hover:underline">
          Download dataset
        </Link>
      </div>

    </section>
  );
}
