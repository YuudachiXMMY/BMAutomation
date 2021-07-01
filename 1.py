import sys, time, random

def WriteProgress(counts: int, total: int, step: int = 1, width: int = 50, unit: str = None):
    '''
    '''
    # sys.stdout.write(' ' * (width + 9) + '\r')
    # sys.stdout.flush()
    progress = int(width * counts / total)
    sys.stdout.write('|' + '█' * progress + ' ' *
                        int(width - progress) + '|')
    if unit is None:
        sys.stdout.write(' {0} / {1}  {2}%\r'.format(int(counts), total, ('%.2f' % (100*counts/total))))
    else:
        sys.stdout.write(' {0} {3} / {1} {3}  {2}%\r'.format(int(counts), total, ('%.2f' % (100*counts/total)), unit))
    if progress == width:
        sys.stdout.write('\n')
    sys.stdout.flush()

def CountProgress(total: int, step: int = 1, width: int = 50, unit: str = None):
    '''
    '''
    for counts in range(0, total+1, step):
        WriteProgress(counts, total, step, width, unit)
        time.sleep(step)

# CountProgress(20, unit="s")

def RandomControlTest(duration: int, width:int = 50) -> None:
    '''
    Perform a random Character Control for games.

    @param:
        - duration: duration to perform the random character control
    '''
    waitTime = 0

    total = duration
    counts = 0
    WriteProgress(counts, total, width=width, unit="s")
    while(duration > 0):

        waitTime = random.uniform(0, 1)
        keyTime = random.uniform(1, 3)

        if keyTime > duration:
            keyTime = int(duration / 2)
            waitTime = duration - keyTime


        duration -= keyTime
        counts += keyTime
        WriteProgress(counts, total, width=width, unit="s")

        time.sleep(waitTime)

        duration -= waitTime
        counts += waitTime
        WriteProgress(counts, total, width=width, unit="s")

RandomControlTest(30)