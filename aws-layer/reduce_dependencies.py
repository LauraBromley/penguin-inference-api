import os
import shutil
import zipfile
import sys
import fileinput

not_required_packages = ['blis','bottleneck','bs4','caffe2','cymem','jsonschema','murmurhash','numexpr','packaging','preshed','scipy',
                          'setuptools','soupsieve','spacy','srsly','thinc','torch','torchvision','tqdm','wasabi']

do_not_remove = ['fastprogress-0.1.21.dist-info']

mpl_subfolders = ['fonts','images','sample_data','stylelib']

def do_reduce(file_path):
    print(file_path)
    root_path = file_path
    package_path = os.path.join(root_path, 'lib', 'python3.6', 'site-packages')
    
    print('Deleting not required packages')
    # remove not required packages
    for package in not_required_packages:
        delete_folder(package_path, package)

    # remove __pycache__
    remove_matching_folders(package_path, '__pycache__')
    # remove test
    remove_matching_folders(package_path, 'tests')
    remove_matching_folders(package_path, 'test')
    # remove dist_info
    remove_matching_folders(package_path, '.dist-info', do_not_remove)
    remove_matching_folders(package_path, '.egg-info', do_not_remove)

    # remove matplotlib mpl_data
    print('Removing matplotlib - mpl-data files (keeping folder structure)')
    matplotlib_subfolder = os.path.join(package_path, 'matplotlib', 'mpl-data')
    for subfolder in mpl_subfolders:
        empty_folder(matplotlib_subfolder, subfolder)

    # edit fastai\imports\core.py file, comment out  "import scipy.stats, scipy.special"
    print('Commenting out scipy import from fastai - imports - core.py (not needed for our application)')
    comment_line_in_file(os.path.join(package_path, 'fastai', 'imports', 'core.py'), 'import scipy.stats, scipy.special')

    #finally zip
    print('Creating zip file')
    zip_contents(root_path)


def comment_line_in_file(filename, line_to_comment):  
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        newlines = []
        for line in lines:
            if line_to_comment in line:
                line = '#{0}'.format(line)
            newlines.append(line)
        file.close()

        file = open(filename, 'w')
        file.writelines(newlines)
        file.close()
    except Exception as e:
        print('Unable to edit file ' + filename)

def zip_contents(folder_path):
    parent_path = os.path.dirname(folder_path)
    zip_path = os.path.join(parent_path, 'fastai-layer.zip')
    archive_from = os.path.dirname(folder_path)
    archive_to = os.path.basename(folder_path.strip(os.sep))
    shutil.make_archive('fastai-layer', 'zip', archive_from, archive_to)
    shutil.move('fastai-layer.zip', zip_path)
    
def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
    except Exception as e: 
        print('Unable to delete ' + folder_path)
        #print(e)

def delete_folder(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    remove_folder(folder_path)

def empty_folder(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    remove_folder(folder_path)
    try:
        os.mkdir(folder_path)
    except Exception as e:
       print('Unable to create ' + folder_path)  
       #print(e)

def remove_matching_folders(path, input, apart_from=[]):
    print('Removing folders matching  ' + input)
    for root, folders, filenames in os.walk(path):
        for folder in folders:
            if folder.endswith(input):
                if folder in apart_from:
                    print('NOT REMOVING ' + os.path.join(root, folder))
                else:    
                    remove_folder(os.path.join(root, folder))         


# entry point
print('Starting...')
args = sys.argv
if len(args) != 2:
    print('Unexpected input - expecting file path to zip file')
else:
    do_reduce(sys.argv[1])

print('Done')
