import os
import shutil


def copy_content_to_folder(source: str, destination: str):
    for name in os.listdir(source):
        path = os.path.join(source, name)
        if not os.path.exists(path):
            continue

        if os.path.isfile(path):
            shutil.copy(path, destination)
            print(f'copied: {path} -> {destination}')

        else:
            dst = os.path.join(destination, name)
            os.mkdir(dst)
            print(f'created: dst')
            copy_content_to_folder(path, os.path.join(destination, name))


def main():
    shutil.rmtree(PATH_TO_PUBLIC)
    os.mkdir(PATH_TO_PUBLIC)

    copy_content_to_folder(PATH_TO_STATIC, PATH_TO_PUBLIC)
    

PATH_TO_PUBLIC = 'public/'
PATH_TO_STATIC = 'static/'
main()

