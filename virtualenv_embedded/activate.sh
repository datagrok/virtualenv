# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly

eval `__VIRTUAL_ENV__/__BIN_NAME__/inve -s`

alias pydoc="python -m pydoc"

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
    hash -r 2>/dev/null
fi
