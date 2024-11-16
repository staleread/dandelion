#!/bin/bash

cat sql/core/schema.sql sql/core/seed.sql sql/dandelion/schema.sql sql/dandelion/seed.sql > db-init.sql

echo "Created db-init.sql by concatenating SQL files"
