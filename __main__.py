from pathlib import Path
from .loader import load_beng_instance

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    print(BASE_DIR)
    file_path = f"{BASE_DIR}/BENG/BENG02.ins2D"
    instance = load_beng_instance(file_path)
    print(instance)
    items = [i.to_list() for i in instance.items]
    print("Items:", items)