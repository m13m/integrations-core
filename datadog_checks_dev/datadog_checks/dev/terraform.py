# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import json
import os
import shutil
from contextlib import contextmanager

import pytest
from six import PY3

from .env import environment_run
from .structures import LazyFunction, TempDir
from .subprocess import run_command
from .utils import chdir

if PY3:
    from shutil import which
else:
    from shutilwhich import which


@contextmanager
def terraform_run(directory, sleep=None, endpoints=None, conditions=None, env_vars=None, wrapper=None):
    """This utility provides a convenient way to safely set up and tear down Docker environments.

    :param directory: A path containing Terraform files.
    :type compose_file: ``str``
    :param sleep: Number of seconds to wait before yielding.
    :type sleep: ``float``
    :param endpoints: Endpoints to verify access for before yielding. Shorthand for adding
                      ``conditions.CheckEndpoints(endpoints)`` to the ``conditions`` argument.
    :type endpoints: ``list`` of ``str``, or a single ``str``
    :param conditions: A list of callable objects that will be executed before yielding to check for errors.
    :type conditions: ``callable``
    :param env_vars: A dictionary to update ``os.environ`` with during execution.
    :type env_vars: ``dict``
    :param wrapper: A context manager to use during execution.
    """
    if not which('terraform'):
        pytest.skip('Terraform not available')

    with TempDir('terraform') as temp_dir:
        terraform_dir = os.path.join(temp_dir, 'terraform')
        shutil.copytree(directory, terraform_dir)
        set_up = TerraformUp(terraform_dir)
        tear_down = TerraformDown(terraform_dir)

        with environment_run(
            up=set_up,
            down=tear_down,
            sleep=sleep,
            endpoints=endpoints,
            conditions=conditions,
            env_vars=env_vars,
            wrapper=wrapper,
        ) as result:
            yield result


class TerraformUp(LazyFunction):
    def __init__(self, directory):
        self.directory = directory

    def __call__(self):
        with chdir(self.directory):
            run_command(['terraform', 'init'], check=True)
            run_command(['terraform', 'apply', '-auto-approve'], check=True)
            output = run_command(['terraform', 'output', '-json'], capture='stdout', check=True).stdout
            return json.loads(output)


class TerraformDown(LazyFunction):
    def __init__(self, directory):
        self.directory = directory

    def __call__(self):
        with chdir(self.directory):
            run_command(['terraform', 'destroy', '-auto-approve'], check=True)
