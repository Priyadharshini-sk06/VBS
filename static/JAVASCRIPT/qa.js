const micBtn = document.getElementById("micBtn");
const chatBox = document.getElementById("qa-chat");

micBtn.onclick = async () => {
  micBtn.innerText = "Listening...";

  const res = await fetch("http://127.0.0.1:5000/qa/listen", {
    method: "POST"
  });

  const data = await res.json();

  micBtn.innerText = "🎤 Ask Question";

  if (data.question) {
    const div = document.createElement("div");
    div.className = "question";
    div.innerText = data.question;
    chatBox.appendChild(div);
  }
};

const exitBtn = document.getElementById("exitBtn");

exitBtn.onclick = async () => {
  await fetch("http://127.0.0.1:5000/mode/sign", {
    method: "POST"
  });

  alert("Back to Sign Detection");
};