# Print iterations progress
def pbar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    # an empty collection has nothing left to do, so show it as complete
    # rather than dividing by zero
    fraction = 1.0 if total == 0 else iteration / float(total)
    percent = ("{0:." + str(decimals) + "f}").format(100 * fraction)
    filledLength = int(length * fraction)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}  ({iteration}/{total})', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

#  init:
#  pbar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)