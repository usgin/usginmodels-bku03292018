#!/bin/sh

/usr/bin/python /usr/lib/ckan/src/usginmodels/usginmodels/model_cache_renewal.py >> /var/log/model_cache_renew.log 2>&1
