from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import pystache

def generate_project(project_name):
    """
    Generate a project by following these steps:

        1. Iterate through the template directory
        2. Replace template variables in path names
        3. Read files
        4. Replace template variables in file contents
        5. Write files to project destination
    """
    project_config = {
        'project_name': project_name,
    }

    # Copy template to current directory
    template_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', 'templates', 'template'))
    project_dir = os.getcwd()

    # Recurse files and directories, replacing their filename with the
    # template string and the file contents with the template strings.
    for root, dirs, files in os.walk(template_dir):
        rel_root = os.path.relpath(root, start=template_dir)
        for dirname in dirs:
            dest_dir = os.path.normpath(os.path.join(project_dir, rel_root, dirname))
            dest_dir = pystache.render(dest_dir, project_config)

            if os.path.exists(dest_dir):
                print('WARN: {} already exists, skipping...'.format(dest_dir))
                continue

            os.mkdir(dest_dir)

        for filename in files:
            src_path = os.path.join(root, filename)

            dest_path = os.path.normpath(os.path.join(project_dir, rel_root, filename))
            dest_path = pystache.render(dest_path, project_config)

            if os.path.exists(dest_path):
                print('WARN: {} already exists, skipping...'.format(dest_path))
                continue

            with open(src_path) as f:
                file_str = f.read()

            file_str = pystache.render(file_str, project_config)

            with open(dest_path, 'w') as f:
                f.write(file_str)

    print('Project created: {}'.format(project_dir))
