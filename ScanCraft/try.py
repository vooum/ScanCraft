#!/usr/bin/env python3
import sys,time
wt=sys.stdout.write
wt('aa\nbb')
sys.stdout.flush()
time.sleep(1)
wt('\r\b\bcc\n')