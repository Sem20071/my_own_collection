#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This module creates a text file with the specified content

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module creates a text file with the specified content

options:
    path:
    description:
      - Path to the file being created
    type: str
    required: true
  content:
    description:
      - File Contents
    type: str
    required: true

author:
    - Aleksandrov Semen
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type="str", required=True),
        content=dict(type="str", required=True)
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        path=path,
        message=''
    )

# Проверяем, существует ли файл
    file_exists = os.path.exists(path)
    
    # Если файл существует, читаем его содержимое
    current_content = ''
    if file_exists:
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except IOError as e:
            module.fail_json(msg=f"Error reading file {path}: {str(e)}", **result)

    # Проверяем, нужно ли менять файл
    content_changed = current_content != content

    if module.check_mode:
        result['changed'] = content_changed or not file_exists
        if content_changed:
            result['message'] = f'File {path} will be changed'
        elif not file_exists:
            result['message'] = f'File {path} will be created'
        else:
            result['message'] = f'File {path} does not require changes'
        module.exit_json(**result)

    # Если файл не существует или содержимое изменилось
    if not file_exists or content_changed:
        try:
            # Записываем содержимое в файл
            with open(path, 'w') as f:
                f.write(content)

            result['changed'] = True
            if not file_exists:
                result['message'] = f'File {path} created'
            else:
                result['message'] = f'File {path} updated'

        except IOError as e:
            module.fail_json(msg=f"File write error {path}: {str(e)}", **result)
        except Exception as e:
            module.fail_json(msg=f"Error while working with file {path}: {str(e)}", **result)

    else:
        result['message'] = f'File {path} does not require changes'
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    # if module.check_mode:
    #     module.exit_json(**result)




    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    # # # # # # result['original_message'] = module.params['name']
    # # # # # # result['message'] = 'goodbye'.format

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    # # # # # if module.params['new']:
    # # # # #     result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # # # # # if module.params['name'] == 'fail me':
    # # # # #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()