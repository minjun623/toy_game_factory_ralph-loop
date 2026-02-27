#!/bin/bash
MAX=1000
mkdir -p logs
for i in $(seq 1 $MAX); do
  echo ""
  echo "========================================"
  echo "  Iteration $i / $MAX - $(date)"
  echo "========================================"
  echo ""
  claude -p "Read PRD.md and follow the instructions. When complete, output DONE." --dangerously-skip-permissions --verbose 2>&1 | tee "logs/iteration-$i.log"
  echo ""
  echo "=== Iteration $i finished at $(date) ==="
  sleep 2
done
echo ""
echo "All $MAX iterations complete!"