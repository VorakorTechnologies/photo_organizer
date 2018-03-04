#! /usr/bin/env python3
import argparse,locale
import os,sys,inspect,re
import datetime,socket,json,traceback

# This file is going to be a class with common functions that manipulate data but don't interact directly with the local machine