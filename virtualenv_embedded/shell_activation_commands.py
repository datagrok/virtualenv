#!__VIRTUAL_ENV__/__BIN_NAME__/python
"""
usage:  $0 SHELL ACTION
Print the commands necessary to perform ACTION in syntax appropriate for SHELL.

This script is expected to be called from various 'activate' scripts, within an
'eval' statement that causes its printed output to be evaluated by the calling
shell. It does not actually do the work of activation or changing any
environment variables.

SHELL may be one of:

    sh          Bourne-shell
    csh         C-shell
    fish        Fish shell

ACTION may be one of:

    backup      Assuming a deactivated virtual environment, print the commands
                to backup environment variables that would be overwritten upon
                activation, if they're not already set.

    activate    Assuming an active virtual environment, print the commands to
                set environment variables that activated it.

    deactivate  Print the commands to restore environment variables from their
                backups.

Examples:

    # Activate virtualenv using sh, bash, zsh, or dash
    eval \`$0 sh backup\`
    eval \`inve $0 sh activate\`

    # Deactivate virtualenv using sh, bash, zsh, or dash
    eval \`$0 sh deactivate\`

    # Activate virtualenv using csh or tcsh
    eval \`$0 csh backup\`
    eval \`inve $0 csh activate\` # csh, tcsh

    # Deactivate virtualenv using csh or tcsh
    eval \`$0 csh deactivate\`

    # Activate virtualenv using fish
    eval $0 fish backup
    eval inve $0 fish activate

    # Deactivate virtualenv using fish
    eval $0 fish deactivate

"""


BACKUP_PREFIX = '_OLD_VIRTUAL_'


# A mapping of shell names to shell syntax dictionaries. A shell syntax
# dictionary maps the keys ['set', 'del', and 'rehash'] to format-strings that
# will be expanded to produce commands compatible with the associated shell.
#
# FIXME: we could do this in a more object-orient-y way with objects and
# inheritance. Would that make this script more (or less) complex/readable?
shells_shell_syntax = {
    'sh': {
        'set': 'export %(key)s="%(value)s";',
        'del': 'unset %(key)s;',
        'rehash': 'hash -r;',
    },
    'csh': {
        'set': 'setenv %(key)s "%(value)s";',
        'del': 'unset %(key)s;',
        'rehash': 'rehash;',
    },
    'fish': {
        'set': 'set -gx %(key)s "%(value)s";',
        'del': 'set -e %(key)s;',
        'rehash': '',
    },
}


def deactivate_commands(env, shell_syntax):
    """Generate the commands needed to "deactivate" a given environment, using
    the given shell-syntax dictionary of format-strings.

    """
    for k in env:
        if k.startswith(BACKUP_PREFIX):
            yield (shell_syntax['set'] % dict(
                key=k[len(BACKUP_PREFIX):],
                value=env[k]))
            yield (shell_syntax['del'] % dict(key=k))


def backup_commands(env, shell_syntax):
    """Generate the commands needed to "back up" the state of a given
    environment in the way that "activate" has traditionally done it, using the
    given shell-syntax dictionary of format-strings.

    """
    for k in ['PATH', 'PYTHONHOME', 'PS1']:
        if k in env and not '%s%s' % (BACKUP_PREFIX, k) in env:
            yield (shell_syntax['set'] % dict(
                key='%s%s' % (BACKUP_PREFIX, k), value=env[k]))


def activate_commands(env, shell_syntax):
    """Using an already-activated environment dictionary for reference,
    generate the commands needed to "activate" the current environment under
    some shell.

    """
    for k in ['PATH', 'PS1']:
        if k in env:
            yield (shell_syntax['set'] % dict(
                key=k, value=env[k]))
    yield (shell_syntax['del'] % dict(key='PYTHONHOME'))
    yield (shell_syntax['rehash'])


def usage(scriptname):
    """Return a usage string"""
    return __doc__.strip().replace('$0', scriptname)


def main(scriptname, shell=None, action=None, *args):
    """Process args and dispatch."""
    import os

    # FIXME TODO: Replace this quick-and-dirty option parsing with optparse.

    actions_generators = {
            'backup': backup_commands,
            'activate': activate_commands,
            'deactivate': deactivate_commands,
            }

    if (shell not in shells_shell_syntax
        or action not in actions_generators
        or args):
        return usage(scriptname)

    shell_syntax = shells_shell_syntax[shell]
    command_generator = actions_generators[action]

    for line in command_generator(os.environ, shell_syntax):
        print(line)

if __name__ == '__main__':
    import sys
    raise SystemExit(main(*sys.argv))
