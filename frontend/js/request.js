const API = "http://127.0.0.1:8000";

async function requestDataset() {
    const gender = document.getElementById("gender").value;
    const age_bucket = document.getElementById("age").value;
    const count = parseInt(document.getElementById("count").value);

    const res = await fetch(`${API}/dataset/request`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({gender, age_bucket, count})
    });

    const data = await res.json();

    document.getElementById("result").innerHTML = `
        <b>Order Created</b><br>
        Request ID: <b>${data.request_id}</b><br>
        ${data.message}
    `;
}
