#!/bin/bash
echo "=== Testing Wiki Update Script ==="

WIKI_REPO="https://github.com/Quality-Assurance-DAO/neo4j.wiki.git"
LOCAL_WIKI_DIR="docs"

echo "1. Would clone from: $WIKI_REPO"
echo "2. Would create local dir: $LOCAL_WIKI_DIR"

# Test directory existence
if [ -d "docs" ]; then
    echo "3. Found docs directory ✓"
    echo "   Contents:"
    ls -la docs/
else
    echo "3. Error: docs directory not found ✗"
fi

# Test git access
echo "4. Testing git access..."
if git ls-remote $WIKI_REPO >/dev/null 2>&1; then
    echo "   Repository is accessible ✓"
else
    echo "   Cannot access repository ✗"
fi

echo "=== Test Complete ==="
