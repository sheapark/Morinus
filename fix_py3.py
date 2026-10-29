# Morinus SE - Python 3 / wxPython 4.2 compatibility patch
# Run from the Morinus folder:  python fix_py3.py
# Originals are copied to  _backup_py3fix/  before any change. Safe to run twice.

import os, re, shutil, glob

SKIP = {'parche_morinus.py', 'fix_py3.py', 'chart_style.py'}
BACKUP = '_backup_py3fix'

def is_comment(line):
    return line.lstrip().startswith('#')

def int_args(m):
    name, args = m.group(1), m.group(2)
    parts = [a.strip() for a in args.split(',')]
    need = {'DrawCircle': 3, 'DrawLine': 4, 'DrawPoint': 2, 'DrawRectangle': 4}[name]
    if len(parts) != need or any(p == '' for p in parts):
        return m.group(0)
    parts = [p if p.startswith('int(') else 'int(%s)' % p for p in parts]
    return '.%s(%s)' % (name, ', '.join(parts))

DRAW_RE = re.compile(r'\.(DrawCircle|DrawLine|DrawPoint|DrawRectangle)\(([^()]*)\)')
TEXTSIZE_RE = re.compile(r'^\s*#\s*([A-Za-z_]\w*)\s*,\s*([A-Za-z_]\w*)\s*=\s*[\w\.]+\.textsize\(')
GETSIZE_RE = re.compile(r'^(\s*)w\s*,\s*h\s*(=\s*get_size\(.*)$')
SIGN_RE = re.compile(r'^(\s*\w+\s*=\s*)([\w\.\[\]]+)\s*/\s*(chart\.Chart\.SIGN_DEG)\s*$')
TRUETYPE_RE = re.compile(r'ImageFont\.truetype\((common\.common\.\w+),\s*(self\.[\w\.]+(?:\s*[/*]\s*[\w\.]+)+)\)')

def fix_lines(fname, lines):
    out = []
    has_predialog = any('wx.PreDialog()' in l for l in lines)
    for i, line in enumerate(lines):
        orig = line
        if not is_comment(line):
            # dict iteration
            line = line.replace('.iteritems()', '.items()').replace('.itervalues()', '.values()').replace('.iterkeys()', '.keys()')
            # list index event
            line = re.sub(r'\b(event|evt)\.m_itemIndex\b', r'\1.GetIndex()', line)
            # sys.maxint
            if 'sys.maxint' in line:
                if re.search(r'self\.Insert\w*Item\(sys\.maxint', line):
                    line = line.replace('sys.maxint', 'self.GetItemCount()')
                else:
                    line = line.replace('sys.maxint', 'sys.maxsize')
            # old wx constructors
            line = line.replace('wx.EmptyBitmap(', 'wx.Bitmap(').replace('wx.EmptyImage(', 'wx.Image(').replace('wx.BitmapFromImage(', 'wx.Bitmap(')
            line = line.replace('.AppendMenu(', '.Append(')
            # PIL
            line = re.sub(r'\.fromstring\(([^()]*\.GetData\(\))\)', r'.frombytes(bytes(\1))', line)
            line = line.replace('.tostring()', '.tobytes()')
            line = TRUETYPE_RE.sub(lambda m: 'ImageFont.truetype(%s, int(max(5, %s)))' % (m.group(1), m.group(2)), line)
            # removed DC methods
            line = re.sub(r'^(\s*)[\w\.]+\.(BeginDrawing|EndDrawing)\(\)\s*$', r'\1pass', line)
            # PreDialog two-step creation
            if has_predialog:
                line = re.sub(r'^(\s*)pre\s*=\s*wx\.PreDialog\(\)\s*$', r'\1wx.Dialog.__init__(self)', line)
                line = re.sub(r'^(\s*)pre\.(SetExtraStyle|Create)\(', r'\1self.\2(', line)
                line = re.sub(r'^(\s*)self\.PostCreate\(pre\)\s*$', r'\1pass', line)
            # wx needs ints for coordinates
            line = DRAW_RE.sub(int_args, line)
            if 'wx.Point(' in line:
                line = re.sub(r'wx\.Point\(self\.w/2,\s*self\.h/2\)', 'wx.Point(self.w//2, self.h//2)', line)
            # sign index must be int
            m = SIGN_RE.match(line.rstrip('\r'))
            if m:
                line = '%sint(%s//%s)' % (m.group(1), m.group(2), m.group(3)) + ('\r' if line.endswith('\r') else '')
            # mis-ported text size variables
            g = GETSIZE_RE.match(line)
            if g and i > 0:
                c = TEXTSIZE_RE.match(lines[i - 1])
                if c and (c.group(1), c.group(2)) != ('w', 'h'):
                    line = '%s%s, %s %s' % (g.group(1), c.group(1), c.group(2), g.group(2))
        out.append(line)
    return out

def special(fname, text):
    if fname == 'limchecklistctrlmixin.py':
        text = text.replace('self.InsertImageStringItem(index, label, 0)', 'self.InsertItem(index, label, 0)')
    if fname == 'graphchartpds.py':
        text = text.replace(
            'li = ((xl, yl, xr, yr), (xr, yr, xm, ym), (xm, ym, xl, yl))',
            'li = [tuple(int(v) for v in t) for t in ((xl, yl, xr, yr), (xr, yr, xm, ym), (xm, ym, xl, yl))]')
    if fname == 'placedb.py':
        if '\nimport wx\n' not in text:
            text = text.replace('import os\nimport pickle\n', 'import os\nimport pickle\nimport wx\nimport mtexts\n', 1)
        text = text.replace("wx.MessageDialog(self, mtexts.txts['DBFileError']", "wx.MessageDialog(None, mtexts.txts['DBFileError']")
    return text

def main():
    if not os.path.exists('morinus.py'):
        print('Morinus 폴더에서 실행해 주세요.')
        return
    os.makedirs(BACKUP, exist_ok=True)
    changed = []
    for fname in sorted(glob.glob('*.py')):
        if fname in SKIP:
            continue
        with open(fname, encoding='utf-8', errors='surrogateescape', newline='') as f:
            text = f.read()
        nl = '\r\n' if '\r\n' in text else '\n'
        lines = text.split(nl)
        new = nl.join(fix_lines(fname, lines))
        new = special(fname, new)
        if new != text:
            bk = os.path.join(BACKUP, fname)
            if not os.path.exists(bk):
                shutil.copy2(fname, bk)
            with open(fname, 'w', encoding='utf-8', errors='surrogateescape', newline='') as f:
                f.write(new)
            changed.append(fname)
    # remove stale bytecode
    shutil.rmtree('__pycache__', ignore_errors=True)
    print('수정한 파일 %d개:' % len(changed))
    for c in changed:
        print('  -', c)
    print('원본 백업 폴더:', BACKUP)

if __name__ == '__main__':
    main()
