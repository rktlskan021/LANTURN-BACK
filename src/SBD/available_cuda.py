import torch

# Check if CUDA is available
if torch.cuda.is_available():
    print("CUDA is available. PyTorch is using GPU.")
    print(f"Device count: {torch.cuda.device_count()}")
    print(f"Current device: {torch.cuda.current_device()}")
    print(f"Device name: {torch.cuda.get_device_name(torch.cuda.current_device())}")
else:
    print("CUDA is not available. PyTorch is using CPU.")
