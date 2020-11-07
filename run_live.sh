#!/usr/bin/env bash

wait-for-it -s -t 300 ${ES_HOST} -- poetry run server
