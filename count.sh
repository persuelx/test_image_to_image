#!/bin/sh
#find $1 -name $2 | wc -l
#ls -lR ./ |grep "*_gt.json*"|wc -l
ls -lR ./ |grep "_gt.json"|wc -l
