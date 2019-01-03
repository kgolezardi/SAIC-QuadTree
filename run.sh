#!/usr/bin/env bash

for ((i=1; i < 20; i++)) do
    python main.py test$i $i
done
