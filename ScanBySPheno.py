#! /usr/bin/env python3
import sys
sys.path.append('/home/vooum/Desktop/ScanCommando')

from command.SPheno import SPheno

S=SPheno(main_routine='./bin/SPhenoNInvSeesaw',in_model='LesHouches.in.NInvSeesaw_low.ES1')