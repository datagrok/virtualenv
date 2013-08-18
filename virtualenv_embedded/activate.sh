# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly

eval `__VIRTUAL_ENV__/__BIN_NAME__/shell_activation_commands sh backup`
eval `__VIRTUAL_ENV__/__BIN_NAME__/inve shell_activation_commands sh activate`

deactivate () {
    eval `__VIRTUAL_ENV__/__BIN_NAME__/shell_activation_commands sh deactivate`
    unset pydoc
    unset -f deactivate
}

alias pydoc="python -m pydoc"
