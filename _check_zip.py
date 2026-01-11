import zipfile
import os

zip_name = "SKLUMToolz_v2.6.6.zip"

if not os.path.exists(zip_name):
    print(f"❌ {zip_name} not found")
else:
    print(f"📂 Contents of {zip_name}:")
    with zipfile.ZipFile(zip_name, 'r') as zipf:
        for info in zipf.infolist():
            print(f"   - {info.filename}")
