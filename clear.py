import os
import shutil

PHOTO_POOL_DIR              = "DCIM"
RAW_DIR                     = "RAW"
RAW_FILE_EXTENSION          = "ARW"   # without the dot"
JPG_DIR                     = "JPG"
JPG_FILE_EXTENSION          = "JPG"   # without the dot"

currentWorkingDir = os.getcwd()

def photoPoolCheck(photoPoolDir, extension):
    fileCount = 0
    if not os.path.isdir(photoPoolDir):
        print("\"" + photoPoolDir + "\" " + "is not a valid path. Attemting to create...")
        try:
            os.makedirs(photoPoolDir, exist_ok=True)
            print("\"" + photoPoolDir + "\" " + "has been created.")
        except Exception as e:
            print(f"Error creating directory: {e}")
    for file in os.listdir(photoPoolDir):
        if file.endswith(extension):
            fileCount += 1
    return fileCount

def moveByType(sourceDir, destinationDir, fileExtension, verbose = False):
    moveCount = 0
    os.makedirs(destinationDir, exist_ok=True)
    filesToMove = [file for file in os.listdir(sourceDir) if file.endswith(fileExtension)]
    for file in filesToMove:
        srcPath = os.path.join(sourceDir, file)
        desPath = os.path.join(destinationDir, file)
        shutil.move(srcPath, desPath)
        if verbose:
            print(f"Moved: {file} -> {destinationDir}")
        moveCount += 1
    return moveCount

def fileCount(dir):    # all extensions
    try:
        return len([file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))])
    except FileNotFoundError:
        print(f"The directory '{dir}' does not exist.")
        return 0

def separateFiles():
    rawCount = photoPoolCheck(PHOTO_POOL_DIR, RAW_FILE_EXTENSION)
    jpgCount = photoPoolCheck(PHOTO_POOL_DIR, JPG_FILE_EXTENSION)
    if rawCount + jpgCount == 0:
        print("Photo pool is empty. Please copy your files into the \"" + PHOTO_POOL_DIR + "\" directory.")
        # return None
    if rawCount == 0:
        print("No RAW to clear. Please check if the \"" + RAW_DIR + "\" directory contains any \"." + RAW_FILE_EXTENSION + "\" files")
        # return None
    if jpgCount == 0:
        print("No JPG detected. Please check if the \"" + JPG_DIR + "\" directory contains any \"." + JPG_FILE_EXTENSION + "\" files")
        # return None
    if fileCount(RAW_DIR) > 0:
        print("Please tidy your \"" + RAW_DIR + "\" directory first.")
        # return None
    if fileCount(JPG_DIR) > 0:
        print("Please tidy your \"" + JPG_DIR + "\" directory first.")
        # return None
    moveByType(PHOTO_POOL_DIR, RAW_DIR, RAW_FILE_EXTENSION, verbose=True)
    moveByType(PHOTO_POOL_DIR, JPG_DIR, JPG_FILE_EXTENSION, verbose=True)
    return None

def removeUnwantedRAW():
    filesNameToKeep = [os.path.splitext(file)[0] 
                       for file in os.listdir(JPG_DIR) 
                       if file.endswith(JPG_FILE_EXTENSION)]
    rawFilesNameList = [os.path.splitext(file)[0] 
                        for file in os.listdir(RAW_DIR) 
                        if file.endswith(RAW_FILE_EXTENSION)]
    filesToRemove = [fileName + "." + RAW_FILE_EXTENSION 
                     for fileName in rawFilesNameList 
                     if fileName not in filesNameToKeep]
    for file in filesToRemove:
        filePath = os.path.join(RAW_DIR, file)
        try:
            os.remove(filePath)
            print(f"File '{filePath}' has been removed.")
        except FileNotFoundError:
            print(f"The file '{filePath}' does not exist.")
        except PermissionError:
            print(f"Permission denied: Cannot remove the file '{filePath}'.")
        except Exception as e:
            print(f"Error removing file '{filePath}': {e}")
    pass

def main():
    separateFiles()
    print("Please remove photos you don't want to keep from the \"" + JPG_DIR + "\" directory then hit enter!")
    input()
    removeUnwantedRAW()
    print("Finish.")

main()