# # Steganography in PNGs
# -------------------------------------------------------------------------------------------------


# ##### *Steganography : practice of hiding a message in another object, in this case a text message in an image*
# -------------------------------------------------------------------------------------------------
# - This program checks to see if the dependencies are installed
# - Runs both a coder and decoder program based on user input
# - Imports and exports files as a PNG
# - Currently this does not support JPEG, due to JPEGs lossieness

# ### Future work
#     - debugging the if/else, there is a small snag that skips the conditional if false
#     - checking if bmp or gif files work
#     - creating a conditional that checks if files are acceptable format, ie PNG or BMP
#     - adding support for Linux and MAC Os

from sys import platform as _platform
import re
import platform
import sys
import os
import subprocess
import pkg_resources
op_sys = os.name
system = platform.system()
release = platform.release()
print(system)
print(release)
print(op_sys)

required = {'opencv-python', 'opencv-contrib-python'}
installed = {pkg.key for pkg in pkg_resources.working_set}
# if 'opencv-python' in list(installed) & 'opencv-contrib-python' in list(installed):
#     print('OpenCV is installed')
missing = required - installed
print(missing)

print('Do you have OpenCV installed? Y or N')
install = input()
if install.lower() == 'no' or install.lower() == 'n':
    if system == 'linux':
        print(f'{system}, {release}')
        print('Chose Pip or -m to Install')
        x =  input()
        if x.lower() == '-m':
            !{sys.executable} -m install opencv-python
            !{sys.executable} -m install opencv-contrib-python
        if x.lower() == 'pip':
            !{sys.executable} -m pip install opencv
            !{sys.executable} -m pip opencv-contrib-python

    elif 'win' in _platform:
        print(f'{system}, {release}')
        !conda install --channel https://conda.anaconda.org/menpo  opencv
        !pip install opencv-contrib-python
        print('Successfully installed OpenCV')
        #Use this code if there is an error
        #!anaconda show menpo/opencv

    elif 'linux' in _platform:
        print(f'{system}, {release}')
        print('Chose Pip or -m to Install')
        x =  input()
        if x.lower() == '-m':
            !{sys.executable} -m install opencv-python
            !{sys.executable} -m install opencv-contrib-python
            print('Successfully installed OpenCV')
        if x.lower() == 'pip':
            !{sys.executable} -m pip install opencv
            !{sys.executable} -m pip opencv-contrib-python
            print('Successfully installed OpenCV')
    else:
        print(f'Operating System {system} not supported')
else:
    import cv2 as cv
    print('\n Continuing program....')
    

#changing message chars to ordinals
def stego_generator(message):
    for char in message:
        #print(f'This is the char: {char}')
        #print(f'This is the ordinal of the char {ord(char)}')
        yield ord(char)

def get_img(img_loc):
    img = cv.imread(img_loc)
    if img is None:
        sys.exit("Could not read the image.")
    #print(img)
    return img

def gcd(x,y):
    while(y):
        x, y = y, x % y
    return x

def encode_stego(img_loc, msg):
    img = get_img(img_loc)
    msg_gen = stego_generator(msg)
    #print(f'This is the message{msg_gen}')
    pattern = gcd(len(img), len(img[0]))
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i+1 * j+1) % pattern == 0:
                #print((i+1 * j+1) % pattern)
                try:
                    img[i-1][j-1][0] = next(msg_gen)
                    #print(f'This is the try line {chr(img[i-1][j-1][0])}')
                except StopIteration:
                    img[i-1][j-1][0] = 0
                    #print(f'This is the image? {img}')
                    return img

def decode_stego(img_loc):
    img = get_img(img_loc)
    pattern = gcd(len(img), len(img[0]))
    message = ''
    print('----------------------------------------------------------------------------')
    print(f'This is the message: {message}')
    print('----------------------------------------------------------------------------')
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i-1 * j-1) % pattern == 0:
                if img[i-1][j-1][0] != 0:
                    #print(f'Numpy array {chr(img[i-1][j-1][0])}')
                    message = message + chr(img[i-1][j-1][0])
                    #print(message)
                else:
                    return message

def format_loc(file_loc):
    try:
        assert os.path.exists(file_loc), 'File not found: ' +str(file_loc)
        f = open(file_loc, 'r+')
        print('File Found, Proceeding...')
        f.close()
        return file_loc
    except AssertionError or PermissionError:
        print('File not found...')

def stegosarus():
    print('For PC')
    choice = input('Code or Decode\n')
    print('Enter the path of your PNG file:\n Example::"C:\\Users\\username\\folder\\filename.png"')
    file_loc = input('-->')
    if format_loc(file_loc):
        if choice.lower() == 'code':
            to_code = input('What is your message?\n')
            encoded_img = encode_stego(file_loc, to_code)
            #cv.imshow("Display window", encoded_img)
            #k = cv.waitKey(5)
            file_name = input('What would you like to call the Image File?\n')
            cv.imwrite(file_name, encoded_img)
        elif choice.lower() == 'decode':
            print(decode_stego(file_loc))
        else:
            print('Command not available')

stegosarus()