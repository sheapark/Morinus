import os, sys, shutil, datetime

APP_SUPPORT = os.path.expanduser('~/Library/Application Support/Morinus')
CHARTS_DIR = os.path.expanduser('~/Documents/Morinus Charts')
LOG_FILE = os.path.expanduser('~/Library/Logs/Morinus.log')

def bundle_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def relink(src, dst):
    if os.path.islink(dst):
        os.remove(dst)
    elif os.path.exists(dst):
        return
    os.symlink(src, dst)

def prepare_workdir(base, home):
    os.makedirs(home, exist_ok=True)
    opts = os.path.join(home, 'Opts')
    os.makedirs(opts, exist_ok=True)
    for name in os.listdir(os.path.join(base, 'Opts')):
        dst = os.path.join(opts, name)
        if not os.path.exists(dst):
            shutil.copy2(os.path.join(base, 'Opts', name), dst)
    res = os.path.join(home, 'Res')
    os.makedirs(res, exist_ok=True)
    for name in os.listdir(os.path.join(base, 'Res')):
        src = os.path.join(base, 'Res', name)
        dst = os.path.join(res, name)
        if name == 'placedb.dat':
            if not os.path.exists(dst) or os.path.islink(dst):
                if os.path.islink(dst):
                    os.remove(dst)
                shutil.copy2(src, dst)
        else:
            relink(src, dst)
    relink(os.path.join(base, 'SWEP'), os.path.join(home, 'SWEP'))
    os.makedirs(CHARTS_DIR, exist_ok=True)
    relink(CHARTS_DIR, os.path.join(home, 'Hors'))

def setup_logging():
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        log = open(LOG_FILE, 'a', buffering=1, encoding='utf-8')
        log.write('\n=== Morinus started %s ===\n' % datetime.datetime.now().isoformat(timespec='seconds'))
        sys.stdout = log
        sys.stderr = log
    except OSError:
        pass

def main():
    setup_logging()
    base = bundle_dir()
    if base not in sys.path:
        sys.path.insert(0, base)
    prepare_workdir(base, APP_SUPPORT)
    os.chdir(APP_SUPPORT)
    sys.argv[0] = os.path.join(APP_SUPPORT, 'morinus')
    import morinus
    app = morinus.Morinus(0)
    app.MainLoop()

if __name__ == '__main__':
    main()
