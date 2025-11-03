#!/bin/bash
#
# Viral Russia News - Complete Automated Workflow
# This script handles the entire daily update process with proper error handling
#

set -e  # Exit on error
set -o pipefail  # Catch errors in pipes

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/workflow_$(date +%Y%m%d_%H%M%S).log"

# Create log directory
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handler
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Change to script directory
cd "$SCRIPT_DIR" || error_exit "Failed to change to script directory"

log "========================================="
log "Viral Russia News - Daily Update Workflow"
log "========================================="

# Step 1: Use existing collected data
log ""
log "[1/5] Using existing collected news data..."
if [ ! -f "data/analyzed_stories.json" ]; then
    log "  Warning: No analyzed stories found"
fi

# Step 2: Analyze stories
log ""
log "[2/5] Analyzing stories and calculating viral scores..."
if python3 analyze_stories.py >> "$LOG_FILE" 2>&1; then
    log "  ✓ Analysis complete"
else
    error_exit "Story analysis failed"
fi

# Step 3: Generate JSON
log ""
log "[3/5] Generating JSON file for web deployment..."
if python3 generate_json.py >> "$LOG_FILE" 2>&1; then
    log "  ✓ JSON generated and validated"
else
    error_exit "JSON generation failed"
fi

# Step 4: Verify JSON file
log ""
log "[4/5] Verifying JSON file..."
if [ -f "public/viral_russia_news.json" ]; then
    SIZE=$(stat -f%z "public/viral_russia_news.json" 2>/dev/null || stat -c%s "public/viral_russia_news.json" 2>/dev/null)
    log "  ✓ File exists (${SIZE} bytes)"
    
    # Validate JSON syntax
    if python3 -m json.tool public/viral_russia_news.json > /dev/null 2>&1; then
        log "  ✓ JSON syntax valid"
    else
        error_exit "Invalid JSON syntax"
    fi
else
    error_exit "JSON file not found"
fi

# Step 5: Commit and push to GitHub
log ""
log "[5/5] Committing and pushing to GitHub..."
git config user.email "bot@manus.im"
git config user.name "Manus Bot"

if git add public/viral_russia_news.json; then
    log "  ✓ File staged"
else
    error_exit "Failed to stage file"
fi

COMMIT_MSG="Auto-update: Viral Russia News - $(date -u +%Y-%m-%d)"
if git diff --cached --quiet; then
    log "  ℹ No changes to commit"
else
    if git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1; then
        log "  ✓ Changes committed"
    else
        error_exit "Commit failed"
    fi
    
    if git push origin main >> "$LOG_FILE" 2>&1; then
        log "  ✓ Pushed to GitHub"
    else
        error_exit "Push failed"
    fi
fi

log ""
log "========================================="
log "✓ Workflow completed successfully!"
log "========================================="
log ""
log "Summary:"
log "  - Log file: $LOG_FILE"
log "  - Site URL: https://viralrussianews.netlify.app/"
log "  - Netlify will auto-deploy in 1-3 minutes"
log ""

exit 0
