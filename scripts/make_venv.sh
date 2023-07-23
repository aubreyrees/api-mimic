#!/usr/bin/env bash


usage()
{
    echo "Usage: $0 [-h] [-r] [-u] [-b <PATH>]
    -r                 Rebuild the venv; use the --clear venv flag
    -u                 Upgrade the venv to use this version of Python
    -b PYTHON_BIN      Use PYTHON_BIN as Python binary
    -h                 Print this message and exit" 1>&2;
}


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd );
source "$SCRIPT_DIR/common.sh";


PYTHON_BIN="python3";
REBUILD=0;
UPGRADE=0;


while getopts "rub:h" o
do
    case "${o}" in
        u)
            UPGRADE=1;
            ;;
        b)
            PYTHON_BIN="${OPTARG}";
            ;;
        h) 
            usage
            exit 0;
            ;;
        r)
            REBUILD=1
            ;;
        *)
            usage
            exit 1;
            ;;
    esac
done


if which "$PYTHON_BIN"  1> /dev/null 2> /dev/null
then
    if [ $REBUILD -eq 1 ]
    then
        if [ $UPGRADE -eq 1 ]
        then
            $PYTHON_BIN -m venv --prompt "$PROMPT" --upgrade-deps --upgrade --clear -- "$VENV_ROOT_PATH";
        else 
            $PYTHON_BIN -m venv --prompt "$PROMPT" --upgrade-deps --clear -- "$VENV_ROOT_PATH";
        fi
    elif [ $UPGRADE -eq 1 ]
    then
        $PYTHON_BIN -m venv --prompt "$PROMPT" --upgrade --upgrade-deps -- "$VENV_ROOT_PATH";
    elif [ ! -d $VENV_ROOT_PATH ]
    then
        $PYTHON_BIN -m venv --prompt "$PROMPT" --upgrade-deps -- "$VENV_ROOT_PATH";
    else
        echo "\`api_mimic_build_venv\` has been set up?";
        exit 1;
    fi
else 
    echo "PYTHON_BIN \`${PYTHON_BIN}\`does not exist?";
    exit 1;
fi
