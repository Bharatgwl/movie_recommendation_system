import gdown
import os

def download_file():
    file_id = '1Ph-PnB2N3TV-cmk4Htc5bE_FSN_rWU1V'  # 👉 Replace this with your actual file ID
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'similarity.pkl'  # The local filename you want to save

    if not os.path.exists(output):
        print("📥 Downloading similarity.pkl...")
        gdown.download(url, output, quiet=False)  # Download the file
    else:
        print("✅ similarity.pkl already exists.")  # If file already exists

# Run the download
download_file()

# https://drive.google.com/file/d/1Ph-PnB2N3TV-cmk4Htc5bE_FSN_rWU1V/view?usp=drive_link