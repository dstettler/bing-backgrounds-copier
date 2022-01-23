import os
import shutil

# Get locations of current directory and the lockscreen images
location = os.getcwd()
bgslocation = os.getenv('LocalAppData') + '\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'

# Create dirs if not already present
if not (os.path.isdir('Lockscreen')):
        os.mkdir('Lockscreen')

if not (os.path.isdir('Desktop')):
        os.mkdir('Desktop')

# Get images already present and the files in the lockscreen directory
bgs = os.listdir(bgslocation)
alreadyHereLock = os.listdir(location + '\\Lockscreen')

print('Copying new files...\n')
subtracted = 0
for bg in bgs:

        # Ensure images already present are not copied
        b = False
        for f in alreadyHereLock:
                split = f.split('.')
                if (split[0] == bg):
                        b = True
                        break
        if b:
                subtracted += 1
                continue
        
        # Get the size of the image and if it is below 100kb don't copy it
        size = os.stat(bgslocation + '\\' + bg).st_size

        if size < 100000:
                subtracted += 1
                continue

        # Copy image
        oldname = bgslocation + '\\' + bg
        newname = location + '\\Lockscreen\\' + bg
        shutil.copy(oldname, newname)

print(f'''Copied {len(bgs) - subtracted} items.''')

files = os.listdir(location + '\\Lockscreen')

print('Files to rename: ')
print(files)
print('\n')

i = 0
for f in files:
        if (f == 'rename.py'):
                continue

        # If a .jpg file is already present, do not rename it
        split = f.split('.')
        if(split[len(split)-1] == 'jpg'):
                continue
        
        size = os.stat('Lockscreen\\' + f).st_size
        print(f)
        print(size)

        # Rename files
        newname = f + '.jpg'
        oldpath = location + '\\Lockscreen\\' + f
        newpath = location + '\\Lockscreen\\' + newname
        os.rename(oldpath, newpath)
        i+=1

print('\nLock screen operations completed.')

# Get files in the desktop wallpaper directory and already present files
binglocation = os.getenv('localappdata') + '\\Microsoft\\BingWallpaperApp\\WPImages'
bingPresent = os.path.isdir(binglocation)
# Make sure bing desktop is actually present before copying files
if bingPresent:
        deskCurrent = os.listdir(location + '\\Desktop')
        bingfiles = os.listdir(binglocation)

        j = 0
        for f in bingfiles:
                # Don't copy unnecessary and already present files
                if (f == 'WPPrefs.bin'):
                        continue

                b = False
                for f2 in deskCurrent:
                        if(f == f2):
                                b = True      
                if b:
                        continue

                # Copy files
                oldname = binglocation + '\\' + f
                newname = location + '\\Desktop\\' + f
                shutil.copy(oldname, newname)
                j += 1


print(f'''\nAll operations completed. {len(files) + j} files processed, and {i} edited.''')
