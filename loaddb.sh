#!/bin/bash

DBNAME=snipper
DDL_DIR=db/

pushd "$DDL_DIR" || exit 1

dropdb "$DBNAME"
createdb "$DBNAME" || exit 1
createlang plpgsql "$DBNAME" || exit 1

ON_ERROR_STOP=1 psql -q "$DBNAME" <<EOF
BEGIN;
\i load_all.psql
COMMIT;
EOF
popd

