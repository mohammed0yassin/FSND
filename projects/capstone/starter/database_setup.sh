#!/bin/bash

PGPASSWORD=12345678 dropdb -U postgres agency_test
PGPASSWORD=12345678 createdb -U postgres agency_test
PGPASSWORD=12345678 psql -U postgres -d agency_test -1 -f agency.psql 1>&1 | grep nothing