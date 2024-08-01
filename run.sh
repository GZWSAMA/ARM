#!/bin/bash

while true
do
    python main.py &
    pid=$!
    wait $pid || echo "main.py exited with failure, restarting..."
done