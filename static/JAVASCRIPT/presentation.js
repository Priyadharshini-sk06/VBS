// ---------------- SPEECH TO TEXT ----------------
let recognition;
let isListening = false;

const transcriptText = document.getElementById("transcriptText");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const spokenLang = document.getElementById("spokenLang");

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

  // TEMP: console log
  // NEXT STEP: connect this to 3D avatar play()
}
