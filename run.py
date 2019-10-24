import json
import logging
import os
import re
import sys

import flywheel
import openslide


# Gear basics
input_folder = 'input/file/'
output_folder = 'output/'


# declare config file path
config_file = 'config.json'

svsfilename = ""


def load_manifest_json():
    """
    load the /flywheel/v0/manifest.json file as a dictionary
    :return: manifest_json
    :rtype: dict
    """
    config_file_path = '/flywheel/v0/manifest.json'
    with open(config_file_path) as manifest_data:
        manifest_json = json.load(manifest_data)
    return manifest_json


def log_initializer(gear_context):
    """
    Generate a log with level and name configured for the suite, gear name and gear-log-level
    :param gear_context: an instance of the flywheel gear context that includes the manifest_json attribute
    :type gear_context: flywheel.gear_context.GearContext
    :return: log
    :rtype: logging.Logger
    """
    log_level = gear_context.config.get('gear-log-level', 'INFO')
    # Set suite (default to flywheel)
    try:
        suite = gear_context.manifest_json['custom']['flywheel']['suite']
    except KeyError:
        suite = 'flywheel'
    # Set gear_name
    gear_name = gear_context.manifest_json['name']
    # Setup logging as per SSE best practices (Thanks Andy!)
    log_name = '/'.join([suite, gear_name])
    # Tweak the formatting
    fmt = '%(asctime)s.%(msecs)03d [%(name)s] %(levelname)-8s: %(message)s'
    logging.basicConfig(level=log_level, format=fmt, datefmt='%H:%M:%S')
    log = logging.getLogger(log_name)
    log.debug('{} log level is {}'.format(log_name, log_level))
    return log


def get_output_path(file_path, output_directory, extension_str='png'):
    """
    Generates a safe path given an input filepath, output directory and optional extension string
    :param file_path: path of the original file
    :type file_path: str
    :param output_directory: directory for output_path
    :type output_directory: str
    :param extension_str: file extension to use (default = 'png')
    :type extension_str: str
    :return:
    """
    # Strip leading .
    extension_str = extension_str.lstrip('.')
    basename = os.path.basename(file_path)
    filename, extension = basename.split('.', maxsplit=1)
    # Make filename safe
    filename = re.sub(r'[^A-Za-z0-9_\-]+', '', filename)
    output_basename = '.'.join(filter(None, [filename, extension_str]))
    output_path = os.path.join(output_directory, output_basename)
    return output_path


def convert_to_png(image_path, output_path, gear_context):
    try:
        gear_context.log.info(f'Opening file: {image_path}')
        s = openslide.OpenSlide(image_path)
    except Exception as e:
        gear_context.log.error(f'ERROR: Exception encountered while opening file {image_path}: {e}')
        os.sys.exit(1)
    try:
        gear_context.log.info(f'Reading region {s.level_count - 1}')
        # t = s.get_thumbnail((512, 512))
        t = s.read_region((0, 0), s.level_count - 1, s.level_dimensions[s.level_count - 1])
    except Exception as e:
        gear_context.log.error(f'ERROR: Exception encountered while reading file region: {e}')
        os.sys.exit(2)

    try:
        gear_context.log.info(f'Saving region to {output_path}')
        t.save(output_path)
    except Exception as e:
        gear_context.log.error(f'ERROR: Exception encountered while saving file to {output_path}: {e}')
        os.sys.exit(3)
    return output_path


def main():
    with flywheel.GearContext() as gear_context:
        # Add manifest.json as the manifest_json attribute
        setattr(gear_context, 'manifest_json', load_manifest_json())
        # Initialize logging
        gear_context.log = log_initializer(gear_context)
        # Log the gear configuration
        gear_context.log.critical('Starting OpenSlide to PNG Converter...')
        gear_context.log.info('Gear configuration:')
        gear_context.log_config()

        input_filepath = gear_context.get_input_path('image')

        output_filepath = get_output_path(input_filepath, gear_context.output_dir)

        convert_to_png(input_filepath, output_filepath, gear_context)
        if os.path.isfile(output_filepath):

            gear_context.log.info('Job completed successfully!!')
            os.sys.exit(0)


if __name__ == '__main__':
    main()



