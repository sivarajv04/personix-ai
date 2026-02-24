const API = "http://127.0.0.1:8000";

async function checkStatus() {
    const rid = document.getElementById("rid").value;

    const res = await fetch(`${API}/dataset/status/${rid}`);
    const data = await res.json();

    let badge = "waiting";
    if(data.status === "completed") badge="ready";
    if(data.status === "processing") badge="processing";
    if(data.status === "failed") badge="failed";

    document.getElementById("status").innerHTML = `
        Status: <span class="badge ${badge}">${data.status}</span><br>
        ${data.message}<br>
        ${data.download_url ? `<a href="download.html?url=${data.download_url}">Go to Download</a>` : ""}
    `;
}
