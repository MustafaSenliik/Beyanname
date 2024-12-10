#!/usr/bin/env bash

host=$1
port=$2
shift 2
cmd="$@"

while ! nc -z $host $port; do
    echo "Waiting for $host:$port to be ready..."
    sleep 2
done

echo "$host:$port is ready. Running command..."
exec $cmd
