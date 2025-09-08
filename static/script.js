async function uploadCharacter() {
    let name = document.getElementById("charName").value;
    let files = document.getElementById("charImages").files;
    let formData = new FormData();
    formData.append("name", name);
    for (let f of files) {
        formData.append("images", f);
    }
    let res = await fetch("/upload", {
        method: "POST",
        body: formData
    });
    alert(await res.text());
    window.location.reload();
}

async function recognizeCharacter() {
    let files = document.getElementById("folderInput").files;
    let formData = new FormData();
    for (let f of files) {
        formData.append("images", f);
    }
    let res = await fetch("/recognize", {
        method: "POST",
        body: formData
    });
    alert(await res.text());
}

function previewImages(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    preview.innerHTML = "";

    if (!input.files) return;

    Array.from(input.files).forEach(file => {
        if (!file.type.startsWith('image/')) return;

        const img = document.createElement("img");
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        img.style.border = "1px solid #ccc";
        img.style.borderRadius = "4px";
        img.style.boxShadow = "0 0 5px rgba(0,0,0,0.2)";
        img.style.cursor = "pointer";

        const reader = new FileReader();
        reader.onload = e => img.src = e.target.result;
        reader.readAsDataURL(file);

        preview.appendChild(img);
    });
}
