export default function DatasetRow({ index, data, update, remove }) {

  const change = (key, value) => {
    update(index, { ...data, [key]: value });
  };

  return (
    <div className="grid md:grid-cols-4 gap-3 items-center bg-black border border-zinc-700 rounded-xl p-4">

      <select
        value={data.gender}
        onChange={e => change("gender", e.target.value)}
        className="p-2 bg-zinc-900 border border-zinc-700 rounded-lg"
      >
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>

      <select
        value={data.age}
        onChange={e => change("age", e.target.value)}
        className="p-2 bg-zinc-900 border border-zinc-700 rounded-lg"
      >
        <option value="0_18">0-18</option>
        <option value="18_25">18-25</option>
        <option value="26_40">26-40</option>
        <option value="40_60">40-60</option>
        <option value="60_plus">60+</option>
      </select>

      <input
        type="number"
        min="1"
        value={data.count}
        onChange={e => change("count", Number(e.target.value))}
        className="p-2 bg-zinc-900 border border-zinc-700 rounded-lg"
        placeholder="Images"
      />

      <button
        onClick={() => remove(index)}
        className="text-red-400 hover:text-red-300"
      >
        Remove
      </button>

    </div>
  );
}
