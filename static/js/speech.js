// LinguaMate AI - Browser Speech Synthesis (TTS) & Web Speech Recognition

class SpeechService {
  constructor() {
    this.synth = window.speechSynthesis;
    this.voices = [];
    this.rate = 0.9;
    this.pitch = 1.0;
    this.isRecording = false;
    this.recognition = null;
    
    this._initVoices();
    this._initRecognition();
  }

  _initVoices() {
    if (!this.synth) return;
    const populate = () => {
      this.voices = this.synth.getVoices().filter(v => v.lang.startsWith("en"));
      if (this.voices.length === 0) {
        this.voices = this.synth.getVoices();
      }
    };
    populate();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = populate;
    }
  }

  _initRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.lang = "en-US";
      this.recognition.interimResults = false;
    }
  }

  speak(text, speed = null) {
    if (!this.synth) {
      alert("Text-to-speech is not supported by your browser.");
      return;
    }

    this.synth.cancel(); // Stop any pending utterance
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = speed !== null ? parseFloat(speed) : this.rate;
    utterance.pitch = this.pitch;

    // Prefer standard English voice
    if (this.voices.length > 0) {
      const preferred = this.voices.find(v => v.name.includes("Natural") || v.name.includes("Google") || v.lang === "en-US") || this.voices[0];
      utterance.voice = preferred;
    }

    this.synth.speak(utterance);
  }

  startRecording(targetText, onResultCallback, onErrorCallback) {
    if (!this.recognition) {
      if (onErrorCallback) onErrorCallback("Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.");
      return;
    }

    try {
      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.trim();
        const similarity = this._calculateSimilarity(targetText.toLowerCase(), transcript.toLowerCase());
        if (onResultCallback) onResultCallback(transcript, similarity);
      };

      this.recognition.onerror = (event) => {
        if (onErrorCallback) onErrorCallback(`Microphone error: ${event.error}`);
      };

      this.recognition.start();
    } catch (e) {
      if (onErrorCallback) onErrorCallback("Could not access microphone.");
    }
  }

  stopRecording() {
    if (this.recognition) {
      this.recognition.stop();
    }
  }

  _calculateSimilarity(str1, str2) {
    // Levenshtein distance based percentage
    const clean1 = str1.replace(/[^\w\s]/gi, '').toLowerCase();
    const clean2 = str2.replace(/[^\w\s]/gi, '').toLowerCase();
    if (clean1 === clean2) return 100;

    const words1 = clean1.split(/\s+/);
    const words2 = clean2.split(/\s+/);
    let matched = 0;
    words1.forEach(w => {
      if (words2.includes(w)) matched++;
    });

    const ratio = (matched / Math.max(words1.length, words2.length)) * 100;
    return Math.round(ratio);
  }
}

window.speechService = new SpeechService();

// Global convenient speak helper for UI buttons
function speakText(text, speed = 0.9) {
  window.speechService.speak(text, speed);
}
