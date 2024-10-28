# Watermarking in LLMs Research Project

This repository contains research materials and code for studying watermarking techniques in Large Language Models (LLMs).

## Project Setup

### Environment Setup
The project uses a Conda environment for dependency management. To set up the environment:

```bash
# Create and activate conda environment from environment.yml
conda env create -f environment.yml
conda activate watermark

# For macOS users, install tesseract using Homebrew
brew install tesseract
```

If you need to update the environment after changes to `environment.yml`:
```bash
conda env update -f environment.yml
```

### API Configuration
Before running the analysis scripts, set up your Anthropic API key:
```bash
# Option 1: Export as environment variable
export ANTHROPIC_API_KEY='your-api-key-here'

# Option 2: Create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

## Data Collection and Processing

### 1. Fetching Paper Abstracts
We've implemented a script to automatically fetch paper abstracts from arXiv. The script:
- Extracts arXiv IDs from markdown files
- Fetches paper information including titles, abstracts, and authors
- Stores the data in structured JSON format

To fetch the abstracts:
```bash
python scripts/fetch_arxiv_abstracts.py
```

The fetched data is stored in [`data/abstract/papers_info.json`](data/abstract/papers_info.
json) with the following structure:
```json
{
  "title": "Paper Title",
  "abstract": "Paper Abstract",
  "authors": ["Author 1", "Author 2"],
  "arxiv_id": "XXXX.XXXXX",
  "url": "https://arxiv.org/abs/XXXX.XXXXX"
}
```

Example of actual fetched data:
```json
{
  "title": "Is Watermarking LLM-Generated Code Robust?",
  "abstract": "We present the first study of the robustness of existing 
  watermarking\ntechniques on Python code generated by large language models. Although 
  existing\nworks showed that watermarking can be robust for natural language, we show 
  that\nit is easy to remove these watermarks on code by 
  semantic-preserving\ntransformations.",
  "authors": [
    "Tarun Suresh",
    "Shubham Ugare",
    "Gagandeep Singh",
    "Sasa Misailovic"
  ],
  "arxiv_id": "2403.17983",
  "url": "https://arxiv.org/abs/2403.17983"
}
```

### 2. PDF Text Extraction
We've implemented a script to extract text from PDF papers using PyMuPDF and Tesseract OCR:
- Processes all PDFs in the `papers/` directory
- Uses PyMuPDF for text extraction
- Falls back to Tesseract OCR for scanned pages
- Saves extracted text in `data/text/` directory
- Maintains detailed logs in `logs/` directory

To process PDFs:
```bash
python scripts/pdf_to_text.py
```

The processing results are stored in:
- `data/text/*.txt`: Extracted text files
- `logs/pdf_processing_*.log`: Processing logs with timestamps

> Note: This implementation uses open-source tools (PyMuPDF and Tesseract) instead of commercial solutions like Mathpix. While this approach is cost-effective, it may not accurately capture mathematical formulas and equations. For research requiring precise mathematical content analysis, consider using specialized OCR services.

## Project Structure
```
.
├── data/
│   ├── abstract/
│   │   └── papers_info.json
│   └── text/
│       └── *.txt
├── results/
│   └── analysis/
│       └── *.json
├── logs/
│   └── *.log
├── papers/
│   └── *.pdf
├── scripts/
│   ├── analyze_papers.py
│   ├── fetch_arxiv_abstracts.py
│   └── pdf_to_text.py
├── environment.yml
└── README.md
```

## Literature Review

### Paper Categories

> Note: The following categorization is generated by Moonshot AI, providing a structured overview of current research directions in LLM watermarking. The classification is based on paper abstracts only, without reviewing the full content of the papers.

> Note: All PDF files in the papers directory are for research purposes only. Please respect the copyright of the original authors and publishers.

1. **Robustness and Detection Capability of Watermarks**:
   - ["Is Watermarking LLM-Generated Code Robust?"](papers/Is_Watermarking_LLM_Generated_Code_Robust.pdf)
   - ["Towards Better Statistical Understanding of Watermarking LLMs"](papers/Towards_Better_Statistical_Understanding_of_Watermarking_LLMs.pdf)
   - ["A Statistical Framework of Watermarks for Large Language Models"](papers/A_Statistical_Framework_of_Watermarks_for_LLMs.pdf)
   - ["No Free Lunch in LLM Watermarking"](papers/Performance_Trade_offs_of_Watermarking.pdf)

2. **Watermark Algorithm Design and Optimization**:
   - ["WatME: Towards Lossless Watermarking Through Lexical Redundancy"](papers/WatME_Towards_Lossless_Watermarking.pdf)
   - ["Topic-Based Watermarks for LLM-Generated Text"](papers/Topic_based_Watermarks_for_LLM_Generated_Text.pdf)
   - ["WaterJudge: Quality-Detection Trade-off when Watermarking Large Language Models"](papers/WaterJudge.pdf)
   - ["Duwak: Dual Watermarks in Large Language Models"](papers/Duwak_Dual_Watermarks.pdf)
   - ["WaterMax: Breaking the LLM Watermark Detectability-Robustness-Quality Trade-off"](papers/WaterMax.pdf)
   - ["Multi-Bit Distortion-Free Watermarking for Large Language Models"](papers/Multi_Bit_Distortion_Free_Watermarking.pdf)
   - ["Provably Robust Multi-bit Watermarking for AI-generated Text"](papers/Provably_Robust_Multi_bit_Watermarking.pdf)
   - ["Instructional Fingerprinting of Large Language Models"](papers/Instructional_Fingerprinting.pdf)
   - ["Adaptive Text Watermark for Large Language Models"](papers/Adaptive_Text_Watermark.pdf)
   - ["Improving the Generation Quality of Watermarked Large Language Models"](papers/Improving_the_Generation_Quality_of_Watermarked.pdf)
   - ["WaterBench: Towards Holistic Evaluation of Watermarks for Large Language Models"](papers/WaterBench.pdf)
   - ["REMARK-LLM: A Robust and Efficient Watermarking Framework"](papers/REMARK_LLM.pdf)
   - ["Embarrassingly Simple Text Watermarks"](papers/Embarrassingly_Simple_Text_Watermarks.pdf)
   - ["Necessary and Sufficient Watermark for Large Language Models"](papers/Necessary_and_Sufficient_Watermark.pdf)
   - ["Functional Invariants to Watermark Large Transformers"](papers/Functional_Invariants_to_Watermark.pdf)
   - ["Watermarking LLMs with Weight Quantization"](papers/Watermarking_LLMs_with_Weight_Quantization.pdf)
   - ["A Semantic Invariant Robust Watermark for Large Language Models"](papers/A_Semantic_Invariant_Robust_Watermark.pdf)
   - ["SemStamp: A Semantic Watermark with Paraphrastic Robustness"](papers/SemStamp.pdf)
   - ["Advancing Beyond Identification: Multi-bit Watermark"](papers/Advancing_Beyond_Identification.pdf)
   - ["Three Bricks to Consolidate Watermarks"](papers/Three_Bricks_to_Consolidate_Watermarks.pdf)
   - ["Towards Codable Watermarking"](papers/Towards_Codable_Text_Watermarking.pdf)
   - ["Robust Distortion-free Watermarks"](papers/Robust_Distortion_free_Watermarks.pdf)
   - ["Watermarking Conditional Text Generation"](papers/Watermarking_Conditional_Text_Generation.pdf)
   - ["Provable Robust Watermarking"](papers/Provable_Robust_Watermarking.pdf)
   - ["Undetectable Watermarks for Language Models"](papers/Undetectable_Watermarks.pdf)
   - ["Watermarking Text Data on Large Language Models"](papers/Watermarking_Text_Data_on_Large_Language_Models.pdf)
   - ["Baselines for Identifying Watermarked Large Language Models"](papers/Baselines_for_Identifying_Watermarked.pdf)
   - ["Who Wrote this Code? Watermarking for Code Generation"](papers/Who_Wrote_this_Code.pdf)
   - ["Robust Multi-bit Natural Language Watermarking"](papers/Robust_Multi_bit_Natural_Language_Watermarking.pdf)
   - ["Are You Copying My Model?"](papers/Are_You_Copying_My_Model.pdf)
   - ["Watermarking Text Generated by Black-Box Language Models"](papers/Watermarking_Text_Generated_by_Black_Box.pdf)
   - ["Protecting Language Generation Models via Invisible Watermarking"](papers/Protecting_Language_Generation_Models.pdf)
   - ["A Watermark for Large Language Models"](papers/A_Watermark_for_Large_Language_Models.pdf)
   - ["Distillation-Resistant Watermarking"](papers/Distillation_Resistant_Watermarking.pdf)
   - ["CATER: Intellectual Property Protection"](papers/CATER.pdf)

3. **Semantic Consistency and Quality Preservation**:
   - ["WatME: Towards Lossless Watermarking Through Lexical Redundancy"](papers/WatME_Towards_Lossless_Watermarking.pdf)
   - ["Improving the Generation Quality of Watermarked Large Language Models"](papers/Improving_the_Generation_Quality_of_Watermarked.pdf)

4. **Cross-lingual and Cross-modal Applications**:
   - ["Can Watermarks Survive Translation?"](papers/Can_Watermarks_Survive_Translation.pdf)

5. **Security and Privacy Issues**:
   - ["WARDEN: Multi-Directional Backdoor Watermarks"](papers/WARDEN.pdf)
   - ["EmMark: Robust Watermarks for IP Protection"](papers/EmMark.pdf)
   - ["Watermarking Text Data on Large Language Models"](papers/Watermarking_Text_Data_on_Large_Language_Models.pdf)

6. **Attack and Defense Mechanisms**:
   - ["Lost in Overlap: Exploring Watermark Collision in LLMs"](papers/Lost_in_Overlap.pdf)
   - ["Evading Watermark based Detection"](papers/Evading_Watermark.pdf)

7. **Evaluation and Benchmarking**:
   - ["WaterJudge: Quality-Detection Trade-off"](papers/WaterJudge.pdf)
   - ["Mark My Words: Analyzing and Evaluating Language Model Watermarks"](papers/Mark_My_Words.pdf)
   - ["WaterBench: Towards Holistic Evaluation of Watermarks"](papers/WaterBench.pdf)

## Paper Analysis

### Analysis Scripts
The project includes scripts for analyzing watermarking papers using Claude API:

```bash
# List available papers
python scripts/analyze_papers.py --list --input-dir data/text

# Analyze a single paper
python scripts/analyze_papers.py --mode single --papers "paper_name" --input-dir data/text

# Analyze multiple papers in batch
python scripts/analyze_papers.py --mode batch --papers "paper1" "paper2" --input-dir data/text
```

### Analysis Modes
1. **Single Paper Analysis**
   - Analyzes one paper at a time
   - Focuses on core contributions and technical details
   - Outputs to `results/analysis/analysis_[paper_name]_[timestamp].json`

2. **Batch Analysis**
   - Compares multiple papers (2-3 recommended)
   - Focuses on unique innovations and comparative strengths
   - Outputs to `results/analysis/batch_analysis_[paper_names]_[timestamp].json`

### Analysis Focus
The analysis particularly emphasizes:
- Key innovations and unique contributions
- Technical uniqueness compared to other approaches
- Comparative strengths and trade-offs

### Output Structure
Analysis results are stored in JSON format with timestamps:
```json
{
  "papers": ["paper1_name", "paper2_name"],
  "analysis": {
    "key_innovation": {
      "unique_contribution": "...",
      "difference_from_existing": "...",
      "novel_problem_solved": "..."
    },
    "technical_uniqueness": {
      "core_advantage": "...",
      "unique_features": "...",
      "special_capabilities": "..."
    },
    "comparative_strengths": {
      "advantages": "...",
      "improvements": "...",
      "trade_offs": "..."
    }
  }
}
```
