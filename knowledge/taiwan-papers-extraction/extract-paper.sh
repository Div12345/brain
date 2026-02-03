#!/bin/bash
# Extract structured data from a single paper using Gemini + Zotero MCP

PAPER_KEY="$1"
OUTPUT_DIR="/home/div/brain/knowledge/taiwan-papers-extraction/papers"

if [ -z "$PAPER_KEY" ]; then
    echo "Usage: $0 <zotero_key>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

PROMPT="You have access to Zotero MCP tools.

TASK: Extract structured information from paper with Zotero key: $PAPER_KEY

STEPS:
1. Use mcp__zotero__zotero_get_item_fulltext with item_key='$PAPER_KEY' to read the full paper
2. Extract ALL of these fields from the paper content:

| Field | Value |
|-------|-------|
| key | $PAPER_KEY |
| citation | Author Year (e.g., Wang 2010) |
| title | Full paper title |
| N | Sample size (number) |
| followup | Follow-up duration (e.g., '15 years' or 'cross-sectional') |
| input_signals | List ALL measurement types (tonometry, oscillometry, PVR, Doppler, etc) |
| signal_locations | List ALL body locations (carotid, femoral, brachial, ankle, radial) |
| derived_variables | List ALL hemodynamic variables calculated (PWV, AI, Pb, cSBP, etc) |
| outcome_type | One of: mortality / surrogate / validation / cross-sectional |
| outcome_variables | What was predicted/validated (death, LV mass, device accuracy, etc) |
| key_finding | Main result with numbers (HR, r, R², AUC, etc) |
| used_ankle_pvr | Yes or No |
| used_brachial_oscillometry | Yes or No |
| multisignal_fusion | Yes or No (combined multiple signal sources) |
| ml_methods | No, or describe method if used (Cox regression doesn't count) |
| mortality_outcome | Yes or No |
| cohort_name | Name of cohort if mentioned (e.g., Chin-Shan, SAPHES) |

OUTPUT: Return ONLY the completed markdown table, nothing else."

echo "Extracting $PAPER_KEY..."
gemini --model gemini-3-pro-preview --prompt "$PROMPT" > "$OUTPUT_DIR/$PAPER_KEY.md" 2>&1

echo "Saved to $OUTPUT_DIR/$PAPER_KEY.md"
