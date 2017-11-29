import os,sys
import glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ngs_scripts.Reference import return_segmentlist
SEGLIST = return_segmentlist('NY238.fa')
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

path = '../FILES/fullvarlist/'
cpath = 'coverage_plots/'
ensure_dir(cpath)

def printfun(thesampleid,SEGMENT,row):
    ntpos = int(row[2])
    major = row[4]
    majorfreq = float(row[5])
    minor = row[6]
    minorfreq = float(row[7])
    binocheck = row[3]
    coverage = float(row[12])  
    covertype = '>1000'
    if int(coverage) <= 200: 
        covertype = '<=200'
    elif int(coverage) <= 1000:
        covertype = '<=1000'

    printlist = [thesampleid,SEGMENT,ntpos,coverage,covertype]
    printlist = [str(x) for x in printlist]
    print>>thefile,','.join(printlist)

for SEGMENT in SEGLIST:
    thefile = open(cpath+SEGMENT+"_coverage_formatted.csv",'w')
    print>>thefile,'sample,segment,ntpos,coverage,covertype'
    for infile in glob.glob( os.path.join(path, '*'+SEGMENT+'.0.01.snplist.csv') ):
        samplename = os.path.basename(infile).split('.')[0]
        print samplename,SEGMENT
        with open(infile,'rU') as f:
            alist = [map(str, line.split(',')) for line in f]
        alist = alist[1:]
        for row in alist:
            printfun(samplename,SEGMENT,row)

