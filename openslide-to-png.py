import sys
import os
import re
import json
import openslide


# Gear basics
input_folder = 'input/file/'
output_folder = 'output/'


# declare config file path
config_file = 'config.json'

svsfilename = ""




print('\n\nStarting OpenSlide to PNG Converter...')

# Read config.json to get eeg filename
with open(config_file) as config_data:
    config = json.load(config_data)
    print('Config:', json.dumps(config, separators=(', ', ': '), sort_keys=True, indent=4))
    svsfilename = config['inputs']['file']['location']['path']

try:
	print('Opening file: ' + svsfilename)
	s = openslide.OpenSlide(svsfilename)
except:
	print('ERROR: Can not open file ' +  svsfilename + '!')
	exit(1)

try:
	print('Reading region ' + str(s.level_count -1))
	#t = s.get_thumbnail((512, 512))
	t = s.read_region((0 ,0), s.level_count -1, s.level_dimensions[s.level_count -1])
except:
	print('ERROR: Can not read file region!')
	exit(2)

try:
	print('Saving region to ' + os.path.join(output_folder, os.path.basename(svsfilename[:-4] + '.png')))
	t.save(os.path.join(output_folder, os.path.basename(svsfilename[:-4] + '.png')))
except:
	print('ERROR: Can not save file ' + os.path.join(output_folder, os.path.basename(svsfilename[:-4] + '.png')))
	exit(3)	

print('\nJob completed successfully!!\n')
exit(0)




