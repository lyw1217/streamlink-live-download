#!/bin/bash
# get options:
IS_CONTAINER=false
while (( "$#" )); do
    case "$1" in
		-c|--container)
			echo "cd /"
			cd /
			URL=/app/target_url.txt
			#SRC=/app/src/main.py
			#if [ -f "$URL" ] && [ -f "$SRC" ]; then  
			#	echo "$URL, $SRC exist "
			#else
			#	echo "/bin/tar -xvf ./app.tar"
			#	/bin/tar -xvf ./app.tar
			#fi
			if [ -f "$URL" ]; then  
				echo "$URL exist"
				/bin/cp $URL ${URL}_bk
			fi
			echo "/bin/tar -xvf ./app.tar"
			/bin/tar -xvf ./app.tar
			
			echo "cd /app"
			cd /app
			echo "IS_CONTAINER=true"
			IS_CONTAINER=true
			shift
			;;
		-*|--*)
            echo "Unsupported flag: $1"
            exit 1
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
