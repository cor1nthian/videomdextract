import subprocess, os, sys

ffmpegfname = 'ffmpeg.exe'
mfpath = '' # media file path
mfmetapath = 'metadata.txt'

# Build ffmpeg and ffprobe from source
# or download at https://www.gyan.dev/ffmpeg/builds/
# or download at https://ffmpeg.org//download.html
# or download at https://mega.nz/file/TAlnSJhC#u58yn-9baEduAXW2dDXLz8YAc_72DC8E0u9J1Wmr6WI
# Only 'bin' folder content needed
# Windows build only

# All tools are suggested to be placed to script folder

# A python class definition for printing formatted text on terminal.
# Initialize TextFormatter object like this:
# >>> cprint = TextFormatter()
#
# Configure formatting style using .cfg method:
# >>> cprint.cfg('r', 'y', 'i')
# Argument 1: foreground(text) color
# Argument 2: background color
# Argument 3: text style
#
# Print formatted text using .out method:
# >>> cprint.out("Hello, world!")
#
# Reset to default settings using .reset method:
# >>> cprint.reset()

class TextFormatter:
    COLORCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7   # white
    }
    FORMATCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }


    # constructor
    def __init__(self):
        self.reset()


    # function to reset properties
    def reset(self):
        # properties as dictionary
        self.prop = {'st': None, 'fg': None, 'bg': None}
        return self


    # function to configure properties
    def cfg(self, fg, bg=None, st=None):
        # reset and set all properties
        return self.reset().st(st).fg(fg).bg(bg)


    # set text style
    def st(self, st):
        if st in self.FORMATCODE.keys():
            self.prop['st'] = self.FORMATCODE[st]
        return self


    # set foreground color
    def fg(self, fg):
        if fg in self.COLORCODE.keys():
            self.prop['fg'] = 30 + self.COLORCODE[fg]
        return self


    # set background color
    def bg(self, bg):
        if bg in self.COLORCODE.keys():
            self.prop['bg'] = 40 + self.COLORCODE[bg]
        return self


    # formatting function
    def format(self, string):
        w = [self.prop['st'], self.prop['fg'], self.prop['bg']]
        w = [str(x) for x in w if x is not None]
        # return formatted string
        return '\x1b[%sm%s\x1b[0m' % (';'.join(w), string) if w else string


    # output formatted string
    def out(self, string):
        print(self.format(string))


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def extractMetadata(mediafilepath: str):
    global ffmpegfname
    global mfmetapath
    if len(mediafilepath) == 0 or mediafilepath is None or not \
        type(mediafilepath) is str:
        return None
    mfpathprepped = mediafilepath
    if ' ' in mfpathprepped:
        mfpathprepped = '"' + mfpathprepped + '"'
    mfpathprepped.replace(' ', '\\ ')
    arglist = [ ffmpegfname,
                '-i',
                mfpathprepped,
                '-f',
                'ffmetadata',
                mfmetapath ]
    arglistjoined = " ".join(arglist)
    process = subprocess.Popen(arglistjoined, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, universal_newlines=True)
    out = process.stdout
    li = 0
    out = []
    for line in process.stdout:
        out.append(line)
    for line in out:
        if len(line.strip()) == 0:
            out.pop(li)
        li += 1
    if os.path.exists(mfmetapath):
        with open(mfmetapath, 'a', encoding='utf-8') as f:
            f.write('\n')
            for line in out:
                f.write(line)
            f.close()
        return 0
    else:
        return None


######### SCRIPT #########
if __name__ == "__main__":
    colorprint = TextFormatter()
    colorprint.cfg('r', 'k', 'b')
    scriptdir = get_script_path()
    ffmpegfname = scriptdir + os.path.sep + ffmpegfname
    mfmetapath = scriptdir + os.path.sep + mfmetapath
    if os.path.exists(mfmetapath):
        os.remove(mfmetapath)
    if not os.path.exists(ffmpegfname):
        colorprint.out('FFMPEG EXE DOES NOT EXIST')
        systemExitCode = 1
        sys.exit(systemExitCode)
    if len(mfpath) == 0 or mfpath is None or not type(mfpath) is str:
        if len(sys.argv) > 1:
            mfpath = sys.argv[1]
        else:
            colorprint.out('MEDIA FILE PATH NOT SET')
            systemExitCode = 2
            sys.exit(systemExitCode)
    else:
        if not os.path.exists(mfpath) :
            colorprint.out('MEDIA FILE PATH DOES BOT EXIST')
            systemExitCode = 3
            sys.exit(systemExitCode)
    retmd = extractMetadata(mfpath)
    if retmd is None:
        colorprint.out('COULD NOT GET MEDIA FILE INFO')
        systemExitCode = 4
        sys.exit(systemExitCode)
    else:
       print('Media info successfully extracted')