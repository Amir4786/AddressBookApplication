import os

folders = [
    "./src",
    "./src/models",
    "./src/schemas",
    "./src/crud",
    "./src/api",
    "./src/core"
]

files = [
    "./src/main.py",
    "./src/database.py",
    "./src/models/address.py",
    "./src/schemas/address.py",
    "./src/crud/address.py",
    "./src/api/address.py",
    "./src/core/logger.py",
    "./src/core/exceptions.py",
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file in files:
    with open(file, "w") as f:
        pass

# Create __init__.py 
for folder in folders:
    init_file = os.path.join(folder, "__init__.py")
    with open(init_file, "w") as f:
        pass

print("FastAPI project structure created!")