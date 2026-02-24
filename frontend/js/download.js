const API = "http://127.0.0.1:8000";

function download() {
    const rid = document.getElementById("rid").value;
    const code = document.getElementById("code").value;

    window.open(`${API}/dataset/download/${rid}/${code}`, "_blank");
}
