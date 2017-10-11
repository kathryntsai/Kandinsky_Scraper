# from urllib.request import urlopen
from bs4 import BeautifulSoup as b
import os
import requests

# get high-res images of art by Wassily Kandinsky and save them to folder 'Kandinsky' in same directory as script

'''750 works are available, numbered 1 through 749.
Instead of using for i in range(1,750):
detect number of files in directory already and then start from there
#files = next(os.walk('Kandinsky'))[2]
#start_i = len(files)
--> not actually using this method
'''

# in future, fix this
# os.chdir('\\Kandinsky')
file_folder = 'Kandinsky\\'

errorCount = 0;
max_errors = 750;

# used to check if file already exists
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return "No match"

for i in range(1, 750):
    
    # need to use this url instead of image url to retrieve title as well
    try:
        url = 'http://www.wassilykandinsky.net/work-' + str(i) + '.php'
        page = requests.get(url).text
        soup = b(page, 'html5lib')
    
        # finds all images in text
        all_img = soup.find_all('img')
    
        # uses the third image
        img = all_img[2]
    
        # get image url and image title
        image = 'http://www.wassilykandinsky.net/' + img.get('src')
        parenthesis = img.get('title').find('(')
        if (parenthesis is None):
            image_name = img.get('title').strip() + '.jpg'
        else:
            image_name = img.get('title')[:parenthesis].strip() +'.jpg'
        
        # makes sure image already exists
        
        if (find(image_name, file_folder)) is 'No match':
            print('saving ', image, ' as ', image_name)
            # save image as image_name in Kandinsky folder
            r = requests.get(image)
            with open(file_folder + image_name, 'wb') as f:
                f.write(r.content)
        else:
            # move onto next work
            print('Work ', str(i), ' has already been saved.')
            quit
            
    except IOError:
        errorCount+=1
        if errorCount > max_errors:
            break
        else:
            print("Error printing Work " + str(i))
    except AttributeError:
        errorCount+=1
        if errorCount > max_errors:
            break
        else:
            print("Cannot find image " + str(i))
            
        
# signals program termination
print ('end')
