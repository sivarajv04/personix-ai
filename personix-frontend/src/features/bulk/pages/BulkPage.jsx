import { useState } from "react";
import BulkBuilder from "../components/BulkBuilder";
import { submitBulkOrder } from "../../../api/bulk";

export default function BulkPage() {

  const [groups, setGroups] = useState([
    { gender: "male", age: "26_40", count: 100 }
  ]);

  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    company: "",
    use_case: "",
    description: ""
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // ---------------- SUBMIT BULK ORDER ----------------
  const handleSubmit = async () => {

    if (!form.name || !form.email || !form.phone) {
      setMessage("Please fill required fields");
      return;
    }

    setLoading(true);
    setMessage("Submitting request...");

    try {

      const payload = {
        name: form.name,
        email: form.email,
        phone: form.phone,
        company: form.company,
        use_case: form.use_case,
        description: form.description,
        dataset_groups: groups.map(g => ({
          gender: g.gender,
          age: g.age,
          count: Number(g.count)
        }))
      };

      await submitBulkOrder(payload);

      setMessage("Request submitted successfully ✓ Our team will contact you.");

      // reset form
      setForm({
        name: "",
        email: "",
        phone: "",
        company: "",
        use_case: "",
        description: ""
      });

      setGroups([{ gender: "male", age: "26_40", count: 100 }]);

    } catch (err) {
      console.error(err);
      setMessage("Submission failed. Check backend.");
    }

    setLoading(false);
  };

  return (
    <main className="max-w-4xl mx-auto px-6 py-24 text-white">

      <h1 className="text-4xl mb-4">Custom Dataset Request</h1>
      <p className="text-zinc-400 mb-10">
        Need large or complex datasets? Configure your dataset requirements below and our team will prepare it manually.
      </p>

      {/* CONTACT */}
      <div className="space-y-4 mb-12">

        <input placeholder="Name"
          value={form.name}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
          onChange={e=>setForm({...form,name:e.target.value})}
        />

        <input placeholder="Email"
          value={form.email}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
          onChange={e=>setForm({...form,email:e.target.value})}
        />

        <input placeholder="Phone"
          value={form.phone}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
          onChange={e=>setForm({...form,phone:e.target.value})}
        />

        <input placeholder="Company (optional)"
          value={form.company}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
          onChange={e=>setForm({...form,company:e.target.value})}
        />

      </div>

      {/* DATASET BUILDER */}
      <h2 className="text-2xl mb-4">Dataset Requirements</h2>
      <BulkBuilder onChange={setGroups} />

      {/* USE CASE */}
      <div className="mt-12 space-y-4">

        <input placeholder="Use case (research, commercial, training...)"
          value={form.use_case}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
          onChange={e=>setForm({...form,use_case:e.target.value})}
        />

        <textarea placeholder="Additional requirements"
          value={form.description}
          className="w-full p-3 bg-black border border-zinc-700 rounded-lg h-32"
          onChange={e=>setForm({...form,description:e.target.value})}
        />

      </div>

      {/* SUBMIT */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-10 w-full bg-purple-600 hover:bg-purple-500 py-4 rounded-xl text-lg disabled:opacity-50"
      >
        {loading ? "Submitting..." : "Submit Bulk Request"}
      </button>

      {/* MESSAGE */}
      {message && (
        <div className="mt-6 text-center text-zinc-300">
          {message}
        </div>
      )}

    </main>
  );
}


// import { useState } from "react";
// import BulkBuilder from "../components/BulkBuilder";
// import { submitBulkOrder } from "../../../api/bulk";


// const API = "http://127.0.0.1:8000";

// export default function BulkPage() {

//   const [groups, setGroups] = useState([
//     { gender: "male", age: "26_40", count: 100 }
//   ]);

//   const [form, setForm] = useState({
//     name:"",
//     email:"",
//     phone:"",
//     company:"",
//     use_case:"",
//     description:""
//   });

//   const [loading, setLoading] = useState(false);
//   const [message, setMessage] = useState("");



//   // ---------------- SUBMIT BULK ORDER ----------------
//   const submitBulk = async () => {

//     if (!form.name || !form.email || !form.phone) {
//       setMessage("Please fill required fields");
//       return;
//     }

//     setLoading(true);
//     setMessage("Submitting request...");

//     try {

//       const res = await fetch(`${API}/bulk/create`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//           ...form,
//           dataset_groups: groups
//         })
//       });

//       const data = await res.json();

//       if (!res.ok) {
//         setMessage(data.detail || "Failed to submit request");
//         setLoading(false);
//         return;
//       }

//       setMessage("Request submitted successfully ✓ Our team will contact you.");

//       // reset form
//       setForm({
//         name:"",
//         email:"",
//         phone:"",
//         company:"",
//         use_case:"",
//         description:""
//       });

//       setGroups([{ gender:"male", age:"26_40", count:100 }]);

//     } catch {
//       setMessage("Server unreachable");
//     }

//     setLoading(false);
//   };

//   const handleSubmit = async () => {
//   try {
//     const payload = {
//       name,
//       email,
//       phone,
//       company,
//       use_case: useCase,
//       description,
//       dataset_groups: groups.map(g => ({
//         gender: g.gender,
//         age: g.age,
//         count: Number(g.count)
//       }))
//     };

//     await submitBulkOrder(payload);

//     alert("Bulk request submitted successfully!");
    
//     // reset form
//     setName("");
//     setEmail("");
//     setPhone("");
//     setCompany("");
//     setUseCase("");
//     setDescription("");
//     setGroups([{ gender: "male", age: "26_40", count: 100 }]);

//   } catch (err) {
//     alert("Submission failed. Check backend.");
//     console.error(err);
//   }
//   };



//   return (
//     <main className="max-w-4xl mx-auto px-6 py-24 text-white">

//       <h1 className="text-4xl mb-4">Custom Dataset Request</h1>
//       <p className="text-zinc-400 mb-10">
//         Need large or complex datasets? Configure your dataset requirements below and our team will prepare it manually.
//       </p>


//       {/* CONTACT */}
//       <div className="space-y-4 mb-12">

//         <input placeholder="Name"
//           value={form.name}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//           onChange={e=>setForm({...form,name:e.target.value})}
//         />

//         <input placeholder="Email"
//           value={form.email}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//           onChange={e=>setForm({...form,email:e.target.value})}
//         />

//         <input placeholder="Phone"
//           value={form.phone}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//           onChange={e=>setForm({...form,phone:e.target.value})}
//         />

//         <input placeholder="Company (optional)"
//           value={form.company}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//           onChange={e=>setForm({...form,company:e.target.value})}
//         />

//       </div>


//       {/* DATASET BUILDER */}
//       <h2 className="text-2xl mb-4">Dataset Requirements</h2>
//       <BulkBuilder onChange={setGroups} />


//       {/* USE CASE */}
//       <div className="mt-12 space-y-4">

//         <input placeholder="Use case (research, commercial, training...)"
//           value={form.use_case}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg"
//           onChange={e=>setForm({...form,use_case:e.target.value})}
//         />

//         <textarea placeholder="Additional requirements"
//           value={form.description}
//           className="w-full p-3 bg-black border border-zinc-700 rounded-lg h-32"
//           onChange={e=>setForm({...form,description:e.target.value})}
//         />

//       </div>


//       {/* SUBMIT */}
//       <button
//         onClick={handleSubmit}
//         disabled={loading}
//         className="mt-10 w-full bg-purple-600 hover:bg-purple-500 py-4 rounded-xl text-lg disabled:opacity-50"
//       >
//         {loading ? "Submitting..." : "Submit Bulk Request"}
//       </button>


//       {/* MESSAGE */}
//       {message && (
//         <div className="mt-6 text-center text-zinc-300">
//           {message}
//         </div>
//       )}

//     </main>
//   );
// }
