library(ggplot2)
# print 'sample,ntpos,majmin,nt,freq,status'
segarr <- c('PB2','PB1','PA','HA','NP','NA','MP','NS')

cpath <- 'coverage_plots/'
for (SEGMENT in segarr){
    filename <- paste(cpath,SEGMENT,'_coverage_formatted.csv',sep='')
    mydata<-read.csv(file=filename,header=T,sep=",")
    
    myColors<-c("#4daf4a","#e41a1c" , "black")
    names(myColors) <- c('>1000','<=1000','<=200')
    colScale <- scale_colour_manual(name = "grp",values = myColors)

    # mydata<-mydata[which(mydata$majmin=='minor'),]
    # FDATA<-mydata[which(mydata$gen==gen),]

    p<- ggplot(mydata,aes(x=factor(ntpos),y=coverage,group=sample,color = covertype)) + geom_line() +#geom_line() +# geom_bar(aes(fill = segment,stat='identity'), colour = "black") + #geom_point(aes(size=freq,alpha=0.8)) +
        # theme(axis.ticks = element_blank(), axis.text.x = element_blank()) +
        theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1,size=8)) +
        facet_wrap(~ sample, ncol = 4, scales = "free") + 
        colScale +
        theme(axis.text.x = element_text(size=8)) +
        scale_x_discrete(breaks=seq(0,max(mydata$ntpos),100))# +
        # ylim(0,5000)

    ggsave(p, file=paste(cpath,SEGMENT,"_coverage_plot.pdf",sep=''), width=14, height=6,limitsize=FALSE)
}   

