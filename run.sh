#!/bin/bash
# get options:
IS_CONTAINER=false
while (( "$#" )); do
    case "$1" in
		-c|--container)
			echo "cd /"
			cd /
			echo "/bin/tar -xvf ./app.tar"
			/bin/tar -xvf ./app.tar

			echo "cd /app"
			cd /app
			echo "IS_CONTAINER=true"
			IS_CONTAINER=true
			shift
			;;
	esac
done

if [ "$IS_CONTAINER" = false ]; then
	echo "source ./.venv/bin/activate"
	source ./.venv/bin/activate
fi

PROGRAM="python"
CMD=`command -v ${PROGRAM} 2>/dev/null`

echo "$CMD ./src/main.py"
$CMD ./src/main.py
