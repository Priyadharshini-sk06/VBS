// ---------------- SPEECH TO TEXT ----------------
let recognition;
let isListening = false;

const transcriptText = document.getElementById("transcriptText");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const spokenLang = document.getElementById("spokenLang");
const pptUpload = document.getElementById("pptUpload");
const slideViewer = document.querySelector(".slide-viewer");

pptUpload.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    const url = URL.createObjectURL(file);

    slideViewer.innerHTML = "";

    // IMAGE
    if (file.type.startsWith("image/")) {

        const img = document.createElement("img");
        img.src = url;
        img.style.width = "100%";
        img.style.height = "100%";
        img.style.objectFit = "contain";

        slideViewer.appendChild(img);
    }

    // PDF
    else if (file.type === "application/pdf") {

        const iframe = document.createElement("iframe");
        iframe.src = url;
        iframe.style.width = "100%";
        iframe.style.height = "100%";

        slideViewer.appendChild(iframe);
    }

    // PPT
    else if (file.name.endsWith(".ppt") || file.name.endsWith(".pptx")) {

        slideViewer.innerHTML = "<p>PPT uploaded successfully (preview not supported here)</p>";

    }

});

startBtn.onclick = () => {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Speech Recognition not supported in this browser");
    return;
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = spokenLang.value;
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onresult = (event) => {
    let finalText = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      if (event.results[i].isFinal) {
        finalText += event.results[i][0].transcript;
      }
    }

    if (finalText.trim() !== "") {
      transcriptText.innerText = finalText;
      processSpeech(finalText);
    }
  };

  recognition.start();
  isListening = true;
};

stopBtn.onclick = () => {
  if (recognition && isListening) {
    recognition.stop();
    isListening = false;
  }
};

// ---------------- SIGN LOGIC ----------------
const WORD_SIGNS = {
  "explain": "EXPLAIN",
  "system": "SYSTEM",
  "architecture": "ARCHITECTURE",
  "project": "PROJECT",
  "model": "MODEL",
  "data": "DATA",
  "ai": "AI",
  "speech": "SPEECH",
  "sign": "SIGN"
};

function processSpeech(text) {
  const clean = text.toLowerCase().replace(/[^a-z\s]/g, "");
  const words = clean.split(" ");

  let sequence = [];

  words.forEach(word => {
    if (WORD_SIGNS[word]) {
      sequence.push(WORD_SIGNS[word]);
    } else {
      word.split("").forEach(letter => {
        sequence.push(letter.toUpperCase());
      });
    }
  });

  console.log("Sign Sequence:", sequence);

  playSequence(sequence);
  function playSequence(sequence) {
    const lang = document.getElementById("signLang").value;
    let delay = 0;

    sequence.forEach(letter => {
        setTimeout(() => {

            const path = `/static/avatar/${lang}/alphabet/${letter}.gif`;

            document.getElementById("signDisplay").src = path;

            console.log("Showing:", path);

        }, delay);

        delay += 900; // adjust speed if needed
    });
 }

  function playSign(sign, lang) {
      let path = `/static/avatar/${lang}/${sign}.gif`;
      document.getElementById("signDisplay").src = path;
      fetch(path)
      .then(res => {
          if (res.ok) {
              playSignAnimation(path);
          } else {
              // fallback to alphabet
              playAlphabet(sign, lang);
          }
      });
  }

  function playAlphabet(word, lang) {
      let delay = 0;

      word.split("").forEach(letter => {
          setTimeout(() => {
              let path = `/static/avatar/${lang}/alphabet/${letter}.gif`;
              document.getElementById("signDisplay").src = path;
          }, delay);

          delay += 800;
      });
  }
}
