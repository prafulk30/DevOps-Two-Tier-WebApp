#!/usr/bin/env bash
set -e

hostport="$1"
shift

if [ -z "$hostport" ]; then
  echo "Usage: $0 host:port -- command"
  exit 1
fi

host=${hostport%:*}
port=${hostport#*:}

echo "Waiting for $host:$port..."

until nc -z "$host" "$port" >/dev/null 2>&1; do
  sleep 1
done

echo "$host:$port is available"

if [ "$1" = "--" ]; then
  shift
  exec "$@"
fi
