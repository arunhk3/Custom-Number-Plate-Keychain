"""Extract glyph outlines from .ttf files into src/fonts.json for the keychain designer."""
import json, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import RecordingPen
CH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.&#@!? abcdefghijklmnopqrstuvwxyz'"
def extract(path, axes=None):
    f = TTFont(path)
    if axes: f = instancer.instantiateVariableFont(f, axes)
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    capH = getattr(f['OS/2'], 'sCapHeight', 0) or int(upm*0.7)
    out = {}
    for c in CH:
        g = cmap.get(ord(c))
        if not g: continue
        p = RecordingPen(); gs[g].draw(p)
        cmds=[]
        for op,args in p.value:
            pts=[round(v,1) for pt in args for v in pt]
            cmds.append([{'moveTo':'M','lineTo':'L','qCurveTo':'Q','curveTo':'C','closePath':'Z','endPath':'Z'}[op]]+pts)
        out[c]={'a':gs[g].width,'d':cmds}
    return {'upm':upm,'cap':capH,'g':out}
from pathlib import Path
# Folder holding the font files. Download from fonts.google.com if needed.
R = str(Path(__file__).resolve().parent.parent / 'fonts') + '/'
fonts={
 'plate': extract(R+'Roboto[wdth,wght].ttf', {'wdth':75,'wght':800}),
 'heavy': extract(R+'Anton-Regular.ttf'),
 'wide':  extract(R+'ArchivoBlack-Regular.ttf'),
}
out = Path(__file__).resolve().parent.parent / 'src' / 'fonts.json'
json.dump(fonts, open(out,'w'), separators=(',',':'))
print('Wrote', out)
