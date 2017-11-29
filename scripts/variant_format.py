import os,sys
import glob
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ngs_scripts.Reference import return_segmentlist
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

cpath = 'comparegraphs/'
ensure_dir(cpath)

STRAIN = 'NY238'
SEGLIST = return_segmentlist('NY238.fa')
MINORFREQ_CUTOFF = 0.01
COVERAGE_CUTOFF = 500
EXCLUDELIST = []
path = '../FILES/fullvarlist/'

def printfun(thesampleid,strain,row,truentlist):
    ntpos = int(row[2])
    major = row[4]
    majorfreq = float(row[5])
    minor = row[6]
    minorfreq = float(row[7])
    binocheck = row[3].upper()
    coverage = float(row[12])  
    nonsyn = row[-1].rstrip()

    covertype = '>1000'
    if int(coverage) <= 200: 
        covertype = '<=200'
    elif int(coverage) <= 1000:
        covertype = '<=1000'

    if ntpos in truentlist:
        #in this case the nonsyn doesn't matter
        printlist = [thesampleid,SEGMENT,ntpos,'major',major,coverage,covertype,''] 
        printlist = [str(x) for x in printlist]
        print>>thefile,','.join(printlist)

        if binocheck == 'TRUE' and minorfreq >= MINORFREQ_CUTOFF and coverage >= COVERAGE_CUTOFF:
            printlist = [thesampleid,SEGMENT,ntpos,'minor',minor,coverage,covertype,nonsyn]
            printlist = [str(x) for x in printlist]
            print>>thefile,','.join(printlist)
        else:
            nonsyn = ''
            printlist = [thesampleid,SEGMENT,ntpos,'minor','',0,covertype,nonsyn]
            printlist = [str(x) for x in printlist]
            print>>thefile,','.join(printlist)



for SEGMENT in SEGLIST:
    print SEGMENT
    unionlist = []

    for infile in glob.glob( os.path.join(path, '*'+SEGMENT+'.0.01.snplist.csv') ):
        samplename = os.path.basename(infile).split('.')[0]
        if samplename in EXCLUDELIST:
            pass
        else:
            strain = os.path.basename(infile).split('.')[1]
            with open(infile,'rU') as f:
                alist = [map(str, line.split(',')) for line in f]
            alist = alist[1:]
            for row in alist:
                ntpos = int(row[2])
                major = row[4]
                majorfreq = float(row[5])
                minor = row[6]
                minorfreq = float(row[7])
                binocheck = row[3].upper()
                coverage = float(row[12])

                if binocheck == 'TRUE' and minorfreq >= MINORFREQ_CUTOFF and coverage >= COVERAGE_CUTOFF:
                    unionlist.append(ntpos)

    unionlist = list(set(unionlist))

    thefile = open(cpath+SEGMENT+"_majorminor_nonsyn_"+str(MINORFREQ_CUTOFF)+"_"+STRAIN+".csv",'w')
    print>>thefile,'sample,segment,ntpos,majmin,nt,coverage,covertype,nonsyn'

    for infile in glob.glob( os.path.join(path, '*'+SEGMENT+'.0.01.snplist.csv') ):
        samplename = os.path.basename(infile).split('.')[0]

        if samplename in EXCLUDELIST:
            pass
        else:
            strain = os.path.basename(infile).split('.')[1]

            with open(infile,'rU') as f:
                alist = [map(str, line.split(',')) for line in f]
            alist = alist[1:]

            for row in alist:
                printfun(samplename,strain,row,unionlist)


