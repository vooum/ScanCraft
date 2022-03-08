#!/usr/bin/env python3

day = 24*60*60
hour = 60*60
minute = 60

def ChangeTime(allTime):
    # if allTime <60:
    #     return  "%d sec"%math.ceil(allTime)
    if  allTime > day:
        days = divmod(allTime,day) 
        return "%ddays, %s"%(int(days[0]),ChangeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime,hour)
        return '%dhour:%s'%(int(hours[0]),ChangeTime(hours[1]))
    elif allTime > minute:
        mins = divmod(allTime,minute)
        return "%dmin:%s"%(int(mins[0]),ChangeTime(mins[1]))
    else: # allTime < 60sec
        return "%.2fsec"%(allTime)


# 从下文修改而来
# ————————————————
# 版权声明：本文为CSDN博主「u010808961」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/u010808961/article/details/38588071