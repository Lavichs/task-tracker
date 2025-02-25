def getColoredText(text, color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m" + text + "\033[0m"
