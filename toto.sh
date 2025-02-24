#!/bin/bash



echo "Removing nvidia_uvm"
if ! rmmod nvidia_uvm; then
    echo "Error: Failed to remove nvidia_uvm module"
    exit 1
fi

echo "Loading nvidia_uvm"
if ! modprobe nvidia_uvm; then
    echo "Error: Failed to load nvidia_uvm module"
    exit 1
fi

echo "Starting ollama again"
if ! systemctl start ollama; then
    echo "Error: Failed to start Ollama service"
    exit 1
fi

echo "Ollama GPU fix applied successfully"
exit 0