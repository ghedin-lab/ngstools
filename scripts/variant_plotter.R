library(ggplot2)
library(reshape)
# print 'sample,segment,ntpos,majmin,nt,freq'

# SEGMENTLIST <- c('PB2','PB1','PA','HA','NP','NA','MP','NS')
# SEGMENTLIST <- c('PB2','PB1','PA','HA','NP','NA')#'MP','NS')
SEGMENTLIST <- c('NY238-HA','NY238-MP','NY238-NA','NY238-NP','NY238-NS','NY238-PA','NY238-PB1','NY238-PB2')
STRAIN <- 'NY238'
cpath <- 'comparegraphs/'

grapher <- function(SEGMENT){
    filename <- paste(cpath,SEGMENT,'_majorminor_nonsyn_0.01_',STRAIN,'.csv',sep='')
    mydata<-read.csv(file=filename,header=T,sep=",",na.strings = c(''))
    # ydiv <- length(unique(mydata$sample))
    # xdiv <- length(unique(mydata$ntpos))

    # FDATA<-mydata[which(mydata$majmin=='minor'),]
    # FDATA<-mydata[which(mydata$gen==gen),]
    # myColors<-c("#4daf4a","#e41a1c" , "black")
    # names(myColors) <- c('>1000','<=1000','<=200')
    # colScale <- scale_colour_manual(name = "grp",values = myColors)

    custom<-c('#d7191c','#ffff33','#1a9641','#2b83ba')
    p<- ggplot(mydata,aes(x=factor(ntpos),y=sample)) + geom_tile(data=subset(mydata,majmin=='major'),aes(fill = nt,alpha=1)) +
    # geom_tile(data=subset(mydata,majmin=='minor'&nonsyn=='syn'),aes(fill = nt),size = 0,height=.5,width=.5)+ #geom_point(data=subset(mydata,majmin=='minor'),aes(size=freq,alpha=0.8)) +
    # geom_tile(data=subset(mydata,majmin=='minor'&nonsyn=='non'),aes(fill = nt),colour='#000000',size = 1,height=.5,width=.5)+ 
    
    geom_tile(data=subset(mydata,majmin=='minor'),aes(fill = nt),size = 0,height=.5,width=.5)+ #geom_point(data=subset(mydata,majmin=='minor'),aes(size=freq,alpha=0.8)) +
    # geom_tile(data=subset(mydata,majmin=='minor'),aes(fill = nt),colour='#000000',size = 1,height=.5,width=.5)+ 

        theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1), 
            panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank()) +
        scale_fill_manual(values=custom)

    ggsave(p, file=paste(cpath,SEGMENT,"_0.01_500_year_nonsyn_",STRAIN,".pdf",sep=''),width=11,height=6,limitsize=FALSE)
 # width=xdiv*1.70, height=ydiv*1.55,
}
for (SEGMENT in SEGMENTLIST){
    grapher(SEGMENT)
}

