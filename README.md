This repository is part of the research project:

# Leveraging Large Language Models for Automated Scalable Development of Open Scientific Databases

If you use this code, models, or experimental pipeline in your research, please cite the paper.

https://arxiv.org/abs/2603.07050

@misc{gautam2026leveraginglargelanguagemodels,
      title={Leveraging Large Language Models for Automated Scalable Development of Open Scientific Databases}, 
      author={Nikita Gautam and Doina Caragea and Ignacio Ciampitti and Federico Gomez},
      year={2026},
      eprint={2603.07050},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/abs/2603.07050}, 
}


# FlaskApp — Literature Scraper + LLaMA-based Filtering (Scopus / ScienceDirect / Web of Science / Google Scholar)

This project is a Flask web app that:

1. Takes a **search equation** (keyword/query) + **year range** + **per-source result limits**.
2. Collects metadata/abstracts from:
   - **Scopus** (Elsevier API)
   - **ScienceDirect** (Elsevier API)
   - **Web of Science (WoS Expanded API)**
   - **Google Scholar** (optional)
3. Merges results, deduplicates (title/DOI), then **filters “relevant” items using a LLaMA prompt-based classifier**.
4. Produces output files (TSV/CSV) and a downloadable zip from the UI.

---

## Project structure

```
FlaskApp/
  app.py                     # Flask routes/UI
  scrapper.py                # Main pipeline: fetch -> merge -> filter
  LLM/zeroshot.py            # LLaMA prompt template / zero-shot classifier logic
  google.py                  # Google Scholar collection
  pyscopus/                  # Scopus/ScienceDirect API client
  WOS/                       # WoS API client helper
  templates/                 # UI pages
  static/                    # UI assets
  bert_classification_model.pth  # (Legacy/optional) BERT weights
```

---

## Requirements

- Python **3.9+** recommended
- API access/keys (depending on which sources you enable):
  - Elsevier (Scopus / ScienceDirect)
  - Web of Science Expanded API
- For **LLaMA filtering**:
  - `transformers`
  - `torch`
  - (Recommended) NVIDIA GPU + CUDA for reasonable speed

---

## Setup

```bash
pip install flask flask-executor pandas numpy torch transformers selenium beautifulsoup4 woslite-client
```

---

## Configure API keys / secrets

This codebase expects API credentials to be available to the runtime (commonly via environment variables or local config inside the code).

Search in `scrapper.py`, `pyscopus/`, and `WOS/` for:
- Elsevier API key usage
- WoS API key usage

Then export them before running (example placeholders):

```bash
export ELSEVIER_API_KEY="..."
export WOS_API_KEY="..."
```

(Exact variable names depend on how you configured the clients in your copy of the repo.)

---

## Run the web app

From the folder that contains `FlaskApp/app.py`:

```bash
cd FlaskApp
python app.py
```

Then open the URL printed in the terminal (commonly `http://127.0.0.1:5000`).

---

## How to use (UI)

1. Go to the home page.
2. Enter:
   - your **search equation**
   - output **alias/folder name** (used as the output directory)
   - year range (**start**, **end**)
   - per-source limits (Scopus/ScienceDirect/WoS/Scholar)
3. Submit the form.
4. The app runs the pipeline and writes outputs under your alias folder.
5. Use the download page to fetch the final zip/output files.

---

## Outputs

Outputs are written under the alias directory you provided in the UI. Typical outputs include:
- per-source “abstracts” files (TSV/CSV)
- merged/deduplicated files
- filtered “selected” files (after LLaMA classification)
- a zip archive for download

File names are constructed in `scrapper.py` (search for `self.alias`, `selected_files`, `final_path`, and per-source output paths).

---

## LLaMA filtering details (high level)

Filtering is done by turning each candidate item (abstract or title) into a prompt like:

- “Given the search equation and the text, return **0** (unrelated) or **1** (related).”

Implementation notes:
- The filtering logic lives in `scrapper.py` (look for the “Filter Using LLAMA2” section) and/or `LLM/zeroshot.py`.
- The model used is configured via `model_id` (e.g., `meta-llama/Llama-2-7b-chat-hf`).
- Device selection is automatic (`cuda` if available, otherwise CPU).

---

## Troubleshooting

- **Selenium errors / ChromeDriver issues**: ensure Chrome + a compatible driver is installed (or switch to a webdriver manager).
- **LLaMA model download is slow**: the first run downloads weights from Hugging Face; subsequent runs should be faster.
- **Out of memory (GPU)**: try CPU, a smaller model, or reduce batch sizes / max tokens in the generation pipeline.
- **API failures**: confirm keys, quotas, and network access.

