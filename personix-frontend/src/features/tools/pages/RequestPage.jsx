import RequestCard from "../../landing/tools/RequestCard.jsx";


export default function RequestPage() {
  return (
    <main className="max-w-3xl mx-auto px-6 py-24">
      <h1 className="text-4xl font-bold mb-10">Request Dataset</h1>

      <RequestCard onCreated={()=>{}} />
    </main>
  );
}
