#!/usr/bin/env python3
"""
Inspect the saved model structure
"""

import torch
import os

# Path to the model
model_path = os.path.join("models", "soil_model2.pth")

print("Inspecting saved model structure...")

try:
    # Load the checkpoint
    checkpoint = torch.load(model_path, map_location='cpu')

    if isinstance(checkpoint, dict):
        if 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
            print("Found 'state_dict' key in checkpoint")
        elif 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
            print("Found 'model_state_dict' key in checkpoint")
        else:
            state_dict = checkpoint
            print("Using entire checkpoint as state_dict")
    else:
        state_dict = checkpoint
        print("Checkpoint is directly a state_dict")

    print(f"\nTotal keys in state_dict: {len(state_dict.keys())}")
    print("\nAll keys in the saved model:")
    for i, key in enumerate(state_dict.keys()):
        print(f"  {i+1:2d}. {key}")

    print(f"\nFC layer keys:")
    fc_keys = [k for k in state_dict.keys() if 'fc' in k]
    for key in fc_keys:
        print(f"  - {key}: shape {state_dict[key].shape}")

except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
