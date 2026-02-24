import { useState } from "react";
import DatasetRow from "./DatasetRow";

export default function BulkBuilder({ onChange = () => {} }) {


  const [rows, setRows] = useState([
    { gender: "male", age: "26_40", count: 100 }
  ]);

  const updateRow = (index, newRow) => {
    const updated = [...rows];
    updated[index] = newRow;
    setRows(updated);
    onChange(updated);
  };

  const removeRow = (index) => {
  if (rows.length === 1) return; // prevent empty crash
  const updated = rows.filter((_, i) => i !== index);
  setRows(updated);
  onChange(updated);
  };


  const addRow = () => {
    const updated = [...rows, { gender: "male", age: "18_25", count: 50 }];
    setRows(updated);
    onChange(updated);
  };

  const total = rows.length
  ? rows.reduce((sum, r) => sum + (Number(r.count) || 0), 0)
  : 0;


  return (
    <div className="space-y-4">

      {rows.map((row, i) => (
        <DatasetRow
          key={i}
          index={i}
          data={row}
          update={updateRow}
          remove={removeRow}
        />
      ))}

      <button
        onClick={addRow}
        className="bg-purple-600 hover:bg-purple-500 px-5 py-2 rounded-lg"
      >
        + Add Dataset Group
      </button>

      <div className="text-right text-zinc-400">
        Total Images: <span className="text-white">{total}</span>
      </div>

    </div>
  );
}
