# AI Study Assistant

A minimal **offline extractive NLP** demo for English PDF/TXT documents. This prototype **does not use a large language model**. It extracts salient sentences and retrieves relevant passages using TF-IDF similarity.

## Run

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open the local Gradio URL (usually http://127.0.0.1:7860). Upload `sample_document.txt`, click **Extract summary**, then ask: `What does the application allow users to upload?`

## Architecture

PDF/TXT upload -> text extraction (pypdf) -> sentence splitting -> frequency-based summarization / TF-IDF retrieval -> Gradio UI.

## Current status and limitations

- Working baseline: English selectable-text PDF/TXT; offline extractive summary and passage retrieval.
- Not implemented: generative LLM, scanned-PDF OCR, hardware acceleration, benchmark results, ASUS UGen / Intel Arc Pro B70 integration.
- Proposed Stage II: integrate an appropriately sized local LLM, optimize inference on Intel Arc Pro B70, evaluate latency and answer faithfulness.
- No claims of tested performance or ASUS hardware compatibility are made.

## Demo

1. Run `python app.py`.
2. Upload `sample_document.txt`.
3. Click **Extract summary**.
4. Go to **Ask document**, enter `What does the application allow users to upload?`, and click **Find answer passages**.

## License

Educational demonstration; no external model weights or proprietary data included.
