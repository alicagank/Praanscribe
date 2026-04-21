# Praanscribe

Please let me know if you use Praanscribe for your research! I feel happy that it helps researchers and I often end up developing features that you suggest! :)
Also, you may cite it as: "Kaya, A. Ç. (2025, May). Praanscribe: A semi-automatic, AI-powered segmentation tool for Praat [Poster presentation]. Student Conference on Linguistics 2025, Boğaziçi University, İstanbul, Türkiye."

**Praanscribe** is an open-source Python CLI application designed to automate the segmentation of parts of speech and the annotation of sounds, as much as possible, using [Praat](http://www.praat.org/). It uses OpenAI’s Whisper model for transcription and produces `.TextGrid` files compatible with Praat for linguistic analysis.

🔗 **https://alicagankaya.com/praanscribe/**

---

## 📌 Purpose & Theoretical Background

**Automatic Speech Recognition (ASR) & Segmentation**

ASR and segmentation technologies are foundational in modern phonetic and phonological research. ASR systems convert spoken input into textual or symbolic representations, making linguistic analysis more efficient (Jurafsky & Martin, 2023). Temporal segmentation—identifying boundaries at the sentence, word, or phoneme level—is key to aligning acoustic signals with linguistic units for qualitative and quantitative research.

**Praat** (Boersma & Weenink, 2001) is a powerful tool for acoustic analysis and manual annotation. It supports multi-tiered `.TextGrid` annotations but requires time-consuming manual effort, especially for large datasets.

**Praanscribe** addresses this challenge by integrating Whisper-based ASR with Praat, generating sentence- and word-aligned `.TextGrid` files automatically—streamlining research workflows and enhancing reproducibility.

---

## ⚙️ Architecture

- Written in **Python**
- Runs **OpenAI’s Whisper** locally
- Supports **5 model sizes**: `tiny`, `base`, `small`, `medium`, and `large`
- Supports **99 languages**
- Automatically generates:
  - Sentence-level and word-level transcriptions
  - `.TextGrid` files aligned with transcription timestamps
  - Grapheme-to-phoneme (G2P) conversion for phonological tiers

> **Note:** As Whisper is corpus-trained, accuracy may drop with pseudowords or rare lexemes. G2P methods work well for standard forms but may not capture dialectal variation.

---

## 🧠 Logic

1. **Transcribe** audio using Whisper (ASR)
2. **Extract** sentence and word timestamps
3. **Convert** data to `.TextGrid` format
4. **Align** tiers in Praat based on user preferences

---

## 🚀 Usage

1. Run the `praanscribe` script in a Python environment.
2. Provide your audio input (`.wav`, `.flac`, `.mp3`, `.aac`, etc.).
3. Choose the Whisper model size (`tiny` to `large`) based on accuracy and compute power.
4. Select tiers to include. Default tiers:
   - `phones`
   - `words-phono`
   - `words`
   - `phono`
   - `ortho`
5. The generated `.TextGrid` file will be saved in the **same directory** as the audio file.

---

## 🎬 Example Output

![Alt text](https://alicagankaya.com/wp-content/uploads/2024/04/Screenshot-2025-04-22-at-21.15.07.png)

---

## 📂 Projects That Use Praanscribe

> These research projects have used Praanscribe and opted to be publicly listed here:

- Kaya, A. Ç. (2024). *Ölçünlü Türkçenin ünlü formant frekansları.* TÜBİTAK 2209-A.
- Uzun, İ. P. (2025). *Türkçede Bileşik Sözcüklerin Sözlü Dilde Üretim Süreçlerine İlişkin Akustik Sesbilgisel Görünümler.* TÜBİTAK 1002-A Hızlı Destek Modülü. (Project No: 223K318)

---

## 📚 References

- Boersma, P. & Weenink, D. (2025). *Praat: doing phonetics by computer* [Computer program]. Version 6.4.27. http://www.praat.org/
- Goldman, J.-P. (2011). *Easyalign: an automatic phonetic alignment tool under praat.* Interspeech 2011, 3233–3236. https://doi.org/10.21437/Interspeech.2011-815
- Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing* (3rd ed.). Draft chapters online.

---

⭐️ Pull requests, issues, and contributions are welcome!
