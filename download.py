import gdown
import os

def download_file():
    # File IDs for the two files
    similarity_file_id = '1Ph-PnB2N3TV-cmk4Htc5bE_FSN_rWU1V'  # similarity.pkl file ID
    movie_dict_file_id = '1B0vBLDuhN52FmYV4Qqlll1MxhVR89ztf'  # movie_dict.pkl file ID
    
    # URLs for the files
    similarity_url = f'https://drive.google.com/uc?id={similarity_file_id}'
    movie_dict_url = f'https://drive.google.com/uc?id={movie_dict_file_id}'
    
    # Output filenames
    similarity_output = 'similarity.pkl'
    movie_dict_output = 'movie_dict.pkl'

    # Download similarity.pkl if not already present
    if not os.path.exists(similarity_output):
        print("📥 Downloading similarity.pkl...")
        gdown.download(similarity_url, similarity_output, quiet=False)
    else:
        print("✅ similarity.pkl already exists.")  # If similarity.pkl already exists

    # Download movie_dict.pkl if not already present
    if not os.path.exists(movie_dict_output):
        print("📥 Downloading movie_dict.pkl...")
        gdown.download(movie_dict_url, movie_dict_output, quiet=False)
    else:
        print("✅ movie_dict.pkl already exists.")  # If movie_dict.pkl already exists

# Run the download function
download_file()

# Links for the files in Google Drive
# similarity.pkl: https://drive.google.com/file/d/1Ph-PnB2N3TV-cmk4Htc5bE_FSN_rWU1V/view?usp=drive_link
# movie_dict.pkl: https://drive.google.com/file/d/1B0vBLDuhN52FmYV4Qqlll1MxhVR89ztf/view?usp=drive_link
