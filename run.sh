#!/bin/bash
SESSION="arcade"

chmod +x loop.sh

# 세션이 이미 있으면 attach, 없으면 새로 만들기
if tmux has-session -t $SESSION 2>/dev/null; then
  tmux attach -t $SESSION
  exit 0
fi

tmux new-session -d -s $SESSION -n loop
tmux send-keys -t $SESSION:loop "./loop.sh" Enter

tmux new-window -t $SESSION -n server
tmux send-keys -t $SESSION:server "python3 -m http.server 8000" Enter

tmux attach -t $SESSION
