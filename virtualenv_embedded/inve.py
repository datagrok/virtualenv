#!__VIRTUAL_ENV__/__BIN_NAME__/python
"""
usage:  $0 [COMMAND [ARG ...]]

Launch COMMAND with ARGs, or the default shell, in the "activated"
virtual environment.

Examples:
    $0                    Launch $SHELL with a modified \$PATH
    $0 screen             Launch screen with a modified \$PATH
    $0 pip install abc    Install 'abc' using the pip inside this venv

"Activating" doesn't mean much; only that the PATH and VIRTUAL_ENV
environment variables have been modified appropriately. If you employ
the full path to the executables in \$VIRTUAL_ENV/bin, you might eschew
this script altogether.

"""

import os, sys


# These values are set to paths specific to the venv when virtualenv creates a
# new venv. FIXME: instead of capturing these and passing them as arguments, we
# could better support --relocatable by parsing the dirname of this script at
# runtime.
virtual_env = '__VIRTUAL_ENV__'
bin_name = '__BIN_NAME__'

# I'd prefer this to live somewhere we can import it, rather than copypasta
# across multiple scripts.
BACKUP_PREFIX = '_OLD_VIRTUAL_'


# FIXME: This instruction may not be correct for all shells. It probably
# belongs within the "shells_shell_syntax" dictionary in shell_commands.py so
# it can be customized based on which shell is being launched.
shell_msg = ("Launching subshell in virtual environment. Type 'exit' or "
             "'Ctrl+D' to return.")


def activate(env, virtual_env, bin_name):
    """Given an environment dictionary env (such as os.environ), "activate" it
    by modifying some of its key/value pairs. This is destructive: it modifies
    its argument and returns None.

    """
    # To avoid the gotcha of having possibly multiple venvs in the PATH, prefer
    # to modify _OLD_VIRTUAL_ENV if it is set, to set the new PATH.
    new_path = os.pathsep.join([
        os.path.join(virtual_env, bin_name),
        env.get('_OLD_VIRTUAL_PATH', env['PATH']),
        ])

    # Backup the environment variables we're about to change, for the
    # convenience of scripts that want to modify their environment in-place.
    # But, only set a backup if one is not set already. (Thus 'deactivate'
    # deactivates all virtualenvs.)
    for key in ['PATH', 'PYTHONHOME']:
        if key in env and '%s%s' % (BACKUP_PREFIX, key) not in env:
            env['%s%s' % (BACKUP_PREFIX, key)] = env[key]

    env['PATH'] = new_path
    env['VIRTUAL_ENV'] = virtual_env
    if 'PYTHONHOME' in env:
        del env['PYTHONHOME']


def invoke(env, args=[]):
    """Launch the user's preferred shell, or a subcommand (given by 'args')"""
    if args:
        return os.execvpe(args[0], args, env)
    else:
        sys.stderr.write('%s\n' % shell_msg)
        return os.execvpe(env['SHELL'], [env['SHELL']], env)


def usage(scriptname, msg=''):
    """Return a usage string with an optional message"""
    return msg + '\n' if msg else '' + __doc__.strip().replace('$0', scriptname)


def main(scriptname, *args):
    """Process args, activate the venv, and dispatch."""
    activate(os.environ, virtual_env, bin_name)
    return invoke(os.environ, args)


if __name__ == '__main__':
   raise SystemExit(main(*sys.argv))
