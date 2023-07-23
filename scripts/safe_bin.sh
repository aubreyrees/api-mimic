#!/usr/bin/env bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd );
source "$SCRIPT_DIR/common.sh";


if [ -d "$VENV_ROOT_PATH/bin" ]
then
    if [ -f "$VENV_ROOT_PATH/bin/$1" ]
    then
        $VENV_ROOT_PATH/bin/$1 "${@:2}";
        exit $?;
    else
        echo "Binary \`$0\` not found in build venv?";
        exit 1;
    fi
else
    echo "\`api_mimic_build_venv\` has not been set up?";
    exit 1;
fi
