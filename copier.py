import datetime
import os
import pathlib
import shutil

# Constants. Sizes measured in bytes.
WHITELISTED_FILETYPES = ['.JPG', '.PNG', '.BMP', '.WEBP']
MIN_LOCK_BG_SIZE = 100000
LOCK_BGS = '\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'
OLD_BING = '\\Microsoft\\BingWallpaperApp\\WPImages'
NEW_BING = '\\Packages\\Microsoft.BingWallpaper_8wekyb3d8bbwe\\LocalState\\images\\Bing'

def genericCopy(src: pathlib.Path, target: pathlib.Path, title: str) -> int:
        files_copied = 0
        if src.exists():
                for f in src.iterdir():
                        if f.suffix.upper() not in WHITELISTED_FILETYPES:
                                continue

                        shutil.copy(f.absolute(), os.path.join(target.absolute(), f.name))
                        files_copied += 1
                print(f'{title} operations completed.')
        else:
                print(f'{title} path not present. Skipping.')

        return files_copied

if __name__ == "__main__":
        # Set path vars
        lock_bgs_location = os.getenv('LocalAppData') + LOCK_BGS
        lock_bgs_path = pathlib.Path(lock_bgs_location)

        old_bing_bgs_location = os.getenv('LocalAppData') + OLD_BING
        old_bing_bgs_path = pathlib.Path(old_bing_bgs_location)

        new_bing_bgs_location = os.getenv('LocalAppData') + NEW_BING
        new_bing_bgs_path = pathlib.Path(new_bing_bgs_location)

        cwd = os.getcwd()
        now = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

        cwd_lockpath = pathlib.Path(os.path.join(cwd, now, 'Lockscreen'))
        cwd_old_deskpath = pathlib.Path(os.path.join(cwd, now, 'Desktop_Old'))
        cwd_deskpath = pathlib.Path(os.path.join(cwd, now, 'Desktop_New'))

        # Create dirs if not already present
        cwd_lockpath.mkdir(parents=True, exist_ok=True)
        cwd_old_deskpath.mkdir(parents=True, exist_ok=True)
        cwd_deskpath.mkdir(parents=True, exist_ok=True)

        # Get images already present and the files in the lockscreen directory
        bgs = os.listdir(lock_bgs_location)
        already_present_lock = os.listdir(cwd_lockpath.absolute())

        files_copied=0

        print('Copying new files...\n')

        # Special case for lock screen files- none of these have file extensions to filter.
        if lock_bgs_path.exists():
                for f in lock_bgs_path.iterdir():
                        if f.stat().st_size < MIN_LOCK_BG_SIZE:
                                continue

                        # Skip anything with a file suffix
                        if ''.join(f.suffixes) != '':
                                continue

                        shutil.copy(f.absolute(), os.path.join(cwd_lockpath.absolute(), f.stem + ".jpg" ))
                        files_copied += 1

                print('Lock screen operations completed.')
        else:
                print('Lock screen path not present. Skipping.')

        files_copied += genericCopy(old_bing_bgs_path, cwd_old_deskpath, 'Old Bing Wallpaper')
        files_copied += genericCopy(new_bing_bgs_path, cwd_deskpath, 'New Bing Wallpaper')

        print(f'\nAll operations completed. {files_copied} files processed.')
