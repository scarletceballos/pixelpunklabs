import os

def find_python_path():
    base = "/Applications/Blender.app/Contents/Resources/4.2"
    python_dir = os.path.join(base, "python")
    
    print(f"\nContents of Python directory:")
    try:
        contents = os.listdir(python_dir)
        for item in contents:
            full_path = os.path.join(python_dir, item)
            print(f"- {item}")
            if os.path.isdir(full_path):
                try:
                    subcontents = os.listdir(full_path)
                    for subitem in subcontents:
                        print(f"  - {subitem}")
                except:
                    pass
    except Exception as e:
        print(f"Error listing directory: {e}")

    # Also check bin directory specifically
    bin_path = os.path.join(python_dir, "bin")
    if os.path.exists(bin_path):
        print(f"\nContents of bin directory:")
        try:
            contents = os.listdir(bin_path)
            for item in contents:
                print(f"- {item}")
        except Exception as e:
            print(f"Error listing bin directory: {e}")

if __name__ == "__main__":
    find_python_path() 