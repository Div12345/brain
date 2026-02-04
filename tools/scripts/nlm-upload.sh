#!/bin/bash
# nlm-upload.sh - Upload sources to NotebookLM
# Usage: nlm-upload.sh <notebook-name> <source-type> <source>
#
# Examples:
#   nlm-upload.sh taiwan-arterial url https://example.com/paper.html
#   nlm-upload.sh ml-science text "Some text content here"
#   nlm-upload.sh stability-selection file /path/to/paper.pdf

set -e

REGISTRY="$HOME/.config/notebooklm/notebooks.yaml"

if [[ $# -lt 3 ]]; then
    echo "Usage: nlm-upload.sh <notebook-name> <source-type> <source>"
    echo ""
    echo "notebook-name: Key from ~/.config/notebooklm/notebooks.yaml"
    echo "source-type:   url | text | file"
    echo "source:        URL, text content, or file path"
    echo ""
    echo "Available notebooks:"
    grep "^  [a-z]" "$REGISTRY" | sed 's/:$//' | sed 's/^  /  - /'
    exit 1
fi

NOTEBOOK_NAME="$1"
SOURCE_TYPE="$2"
SOURCE="$3"

# Get notebook ID from registry
NOTEBOOK_ID=$(python3 -c "
import yaml
with open('$REGISTRY') as f:
    reg = yaml.safe_load(f)
nb = reg.get('notebooks', {}).get('$NOTEBOOK_NAME')
if nb:
    print(nb['id'])
else:
    print('NOT_FOUND')
")

if [[ "$NOTEBOOK_ID" == "NOT_FOUND" ]]; then
    echo "Error: Notebook '$NOTEBOOK_NAME' not found in registry"
    exit 1
fi

echo "Uploading to notebook: $NOTEBOOK_NAME ($NOTEBOOK_ID)"
echo "Source type: $SOURCE_TYPE"

# Use Claude to run the MCP tool
case "$SOURCE_TYPE" in
    url)
        echo "URL: $SOURCE"
        echo "Run in Claude: source_add(notebook_id='$NOTEBOOK_ID', source_type='url', url='$SOURCE', wait=True)"
        ;;
    text)
        echo "Text content (first 50 chars): ${SOURCE:0:50}..."
        echo "Run in Claude: source_add(notebook_id='$NOTEBOOK_ID', source_type='text', text='...', title='Title', wait=True)"
        ;;
    file)
        echo "File: $SOURCE"
        if [[ ! -f "$SOURCE" ]]; then
            echo "Error: File not found: $SOURCE"
            exit 1
        fi
        echo "Run in Claude: source_add(notebook_id='$NOTEBOOK_ID', source_type='file', file_path='$SOURCE', wait=True)"
        ;;
    *)
        echo "Error: Unknown source type: $SOURCE_TYPE"
        echo "Valid types: url, text, file"
        exit 1
        ;;
esac

echo ""
echo "Note: This script shows the command. Run it in a Claude session with NotebookLM MCP."
