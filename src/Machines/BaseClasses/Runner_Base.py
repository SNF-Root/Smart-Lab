from src.uploader import Uploader

from datetime import datetime
import timeit
import os
import shutil
import hashlib
from abc import ABC, abstractmethod



class Runner_Base(ABC):

    def __init__(self):
        pass

    
    def changeName(self, filepath, append):
        """
        Changes the name of a file by appending a string to the file name.
            
            Parameters
            -----------
                filepath: str
                    the path to the file to be renamed
                append: str
                    the string to append to the file name
            Returns
            -------
                str
                    the new path to the renamed file
        """
        # RENAME FILE
        name = os.path.basename(filepath)
        newpath = filepath.replace(name, f"({append}) {name}")
        # CHANGE FILE NAME
        try:
            os.rename(filepath, newpath)
        except:
            print("Error: File not found, Rename failed")
            raise FileNotFoundError("File not found, Rename failed")
        return newpath
    

    def copy_item(self, src, dst):
        """
        Copy an item (file or directory) from src to dst.
        
            Parameters
            -----------
                src: str
                    the path to the source item
                dst: str
                    the path to the destination item

            Returns
            -------
                None
        """
        if os.path.isdir(src):
            try:
                shutil.copytree(src, dst, dirs_exist_ok=True)
            except FileNotFoundError as e:
                raise e
        else:
            try:
                shutil.copy2(src, dst)
            except FileNotFoundError as e:
                raise e
            
    
    def copy_sources_to_new_folder(self, src_items, base_dst_folder):
        """
        Copies the contents of source items (files or folders) to a new folder in base_dst_folder.
        The new folder is named according to the current date and time.

            Parameters
            -----------
                src_items: list
                    a list of paths to the source items
                base_dst_folder: str
                    the path to the base destination folder

            Returns
            -------
                str: the name of the new folder created
        """
        # Create the new folder name
        dirname = datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
        dst_folder = os.path.join(base_dst_folder, dirname)
        
        try:
            # Create destination folder
            os.makedirs(dst_folder, exist_ok=True)
            
            # Copy the contents of the source items to the destination folder
            for src in src_items:
                if not os.path.exists(src):
                    raise FileNotFoundError(f"Source item '{src}' does not exist.")
                
                item_name = os.path.basename(src)
                dst_item = os.path.join(dst_folder, item_name)
                self.copy_item(src, dst_item)
            
            print(f"Contents of {src_items} have been copied to '{dst_folder}'.")
            return dirname

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        

    def copy_folder_contents(self, name, src_folder1, src_folder2, base_dst_folder):
        """
        Copies the contents of src_folder1 and src_folder2 to a new folder in base_dst_folder.
        The new folder is named according to the current date and time.

            Parameters
            -----------
                src_folder1: str
                    the path to the first source folder
                src_folder2: str
                    the path to the second source folder
                base_dst_folder: str
                    the path to the base destination folder
            
            Returns
            -------
                str: the name of the new folder created
        """
        # Create the new folder name
        dirname = name + "~" + datetime.now().strftime("%m:%d:%Y") + "~" + datetime.now().strftime("%H:%M")
        dst_folder = os.path.join(base_dst_folder, dirname)
        
        try:
            # Check if source folders exist
            if not os.path.exists(src_folder1):
                raise FileNotFoundError(f"Source folder '{src_folder1}' does not exist.")
            if not os.path.exists(src_folder2):
                raise FileNotFoundError(f"Source folder '{src_folder2}' does not exist.")
            
            # Create destination folder
            os.makedirs(dst_folder, exist_ok=True)
            
            # Copy the contents of the first source folder to the destination folder
            for item in os.listdir(src_folder1):
                src_item = os.path.join(src_folder1, item)
                dst_item = os.path.join(dst_folder, item)
                
                if os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_item, dst_item)
            
            # Copy the contents of the second source folder to the destination folder
            for item in os.listdir(src_folder2):
                src_item = os.path.join(src_folder2, item)
                dst_item = os.path.join(dst_folder, item)
                
                if os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_item, dst_item)
            
            print(f"Contents of '{src_folder1}' and '{src_folder2}' have been copied to '{dst_folder}'.")
            return dirname

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e


    def calculate_checksum(self, dataPath):
        """
        Calculate the checksum of the file contents.
        
            Parameters
            -----------
                file_path: str
                    The path to the file to calculate the checksum for.

            Returns
            -------
                str: The checksum of the file contents.
        """
        with open(dataPath, 'rb') as file:
            file_content = file.read()
            return hashlib.md5(file_content).hexdigest()
        

    @abstractmethod
    def run(self):
        """
        Runs the algorithms for all machines of this type and uploads the results to the cloud storage.
        Handles checksums, ensures files are matching and new.
        Handles raw file transfer algorithms

            Parameters
            -----------
                None
            
            Returns
            -------
                None
        """
        pass


def main():
    return


if __name__ == "__main__":
    main()