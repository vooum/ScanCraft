#!/usr/bin/env python3

import argparse
parserer=argparse.ArgumentParser(prog='Transfer_Files')

parserer.add_argument('--version','-V', action='version', version='%(prog)s 0.01')

parserer.parse_args()