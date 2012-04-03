#!__VIRTUAL_ENV__/__BIN_NAME__/python
"""
usage:  $0 [COMMAND [ARG ...]]
    or:  eval \`$0 -s\` # sh, bash, zsh, dash
    or:  eval \`$0 -c\` # csh, tcsh
    or:  eval $0 -f # fish
Launch COMMAND with ARGs, or the default shell, in the "activated"
virtual environment. Or, print shell statements that, if evaluated,
would cause the current environment to become activated.

The shell language to be used is selected by one of the following
options:
    -s, --shell=sh        Bourne-shell
    -c, --shell=csh       C-shell
    -f, --shell=fish      Fish shell

Examples:
    $0                    Launch $SHELL with a modified \$PATH
    $0 screen             Launch screen with a modified \$PATH
    $0 pip install abc    Install 'abc' using the pip inside this venv
    eval \`$0 -s\`          If using bash, modify \$PATH in your current environment

"Activating" doesn't mean much; only that the PATH and VIRTUAL_ENV
environment variables have been modified appropriately. If you employ
the full path to the executables in \$VIRTUAL_ENV/bin, you might eschew
this script altogether.

"""

import os, sys


virtual_env = '__VIRTUAL_ENV__'
bin_name = '__BIN_NAME__'


# FIXME: This instruction may not be correct for all shells. It probably
# belongs within the "shellcommands" dictionary so it can be customized based
# on which shell is being launched.
shell_msg = ("Launching subshell in virtual environment. Type 'exit' or "
             "'Ctrl+D' to return.")


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
    }
}


def activate(env, virtual_env, bin_name):
    """Given an environment dictionary env (such as os.environ), "activate" it
    by modifying some of its key/value pairs.

    """
    env['VIRTUAL_ENV'] = virtual_env
    env['PATH'] = os.pathsep.join([
            os.path.join(virtual_env, bin_name),
            env['PATH'],
        ])
    if 'PYTHONHOME' in env:
        del env['PYTHONHOME']


def deactivate_commands(env, shell_syntax):
    """Generate the commands needed to "deactivate" a given environment, using
    the given shell-syntax dictionary of format-strings.

    """
    for k in ['PATH', 'PYTHONHOME', 'PS1']:
        if '_OLD_VIRTUAL_%s' % k in env:
            yield (shell_syntax['set'] % dict(
                key=k, value=env['_OLD_VIRTUAL_%s' % k]))
            yield (shell_syntax['del'] % dict(
                key='_OLD_VIRTUAL_%s' % k))


def backup_commands(env, shell_syntax):
    """Generate the commands needed to "back up" the state of a given
    environment in the way that "activate" has traditionally done it, using the
    given shell-syntax dictionary of format-strings.

    """
    for k in ['PATH', 'PYTHONHOME', 'PS1']:
        if k in env and not '_OLD_VIRTUAL_%s' % k in env:
            yield (shell_syntax['set'] % dict(
                key='_OLD_VIRTUAL_%s' % k, value=env[k]))


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


def invoke(args=[], newenv):
    """Launch the user's preferred shell, or a subcommand (given by 'args')"""
    if args:
        os.execvp(args[0], args, newenv)
    else:
        sys.stderr.write('%s\n' % shell_msg)
        os.execvp(os.environ['SHELL'], [os.environ['SHELL']])


def usage(scriptname, msg=''):
    """Return a usage string with an optional message"""
    return msg + '\n' if msg else '' + __doc__.strip().replace('$0', scriptname)


def main(scriptname, *args):
    """Process args and dispatch."""

    # FIXME TODO: Replace this quick-and-dirty option parsing with optparse.

    if args and args[0].startswith('-'):
        # In this mode, we modify the user's *current* environment by printing
        # commands in the language of whatever shell the user is using. The
        # user is expected to ask their shell to capture and evaluate these
        # commands.
        option = args[0]

        if option in ['-h', '--help']:
            return usage(scriptname)

        if option in ['-s', '--shell=sh']:
            shell = 'sh'
        elif option in ['-c', '--shell=csh']:
            shell = 'csh'
        elif option in ['-f', '--shell=fish']:
            shell = 'fish'
        else:
            return usage(scriptname, "Unknown option.")

        shell_syntax = shells_shell_syntax[shell]

        if scriptname.endswith('deactivate'):
            # reset to the user's original enironment using the "backup" keys
            # in the environment.
            for line in deactivate_commands(os.environ, shell_syntax):
                print(line)
        else:
            # create "backup" keys if they don't already exist, then activate
            for line in backup_commands(os.environ, shell_syntax):
                print(line)
            activate(os.environ, virtual_env, bin_name)
            for line in activate_commands(os.environ, shell_syntax):
                print(line)

    else:
        # In this mode, we invoke a command with a modified environment, which
        # skips all the contortion we do with shell syntaxes and deactivation.
        # When the command exits, the user's current environment is unmodified.
        activate(os.environ, virtual_env, bin_name)
        return invoke(args)


if __name__ == '__main__':
   raise SystemExit(main(*sys.argv))
