# Copyright (C) 2016 Greenweaves Software Pty Ltd
#
# simon@greenweaves.nz
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

# Code to suppport term=project.Rmd

library(data.table)

get.file.name<-function(prefix,reading,date,adj,tar='tar',gz='gz') {
  return (paste(prefix,reading,date,adj,tar,gz,sep='.')) 
}

my.untar<-function (file,list=TRUE,out.path='.\\data', program='C:\\7z1604-extra\\7za',cmd='e',clean=TRUE){
  untar.command<-function(file.name){
    system(sprintf('%s %s %s -o%s -y',program,cmd,file.name,out.path))
  }
 
  untar.command(file)
  tar.file<-sub('.gz$','',file)
  untar.command(tar.file)
  if (clean) {
    file.remove(file)
    file.remove(tar.file)
  }
  parts<-unlist(strsplit(basename(file),'.',fix=TRUE))
  pattern<-sprintf('%s.%s.*%s.((dat)|(inv))',parts[1],parts[2],parts[4])
  files<-list.files(out.path,pattern=pattern)
  return (lapply(files,function(x){return (file.path(out.path,x))}))
}

download.temperature.data<-function(
  data.path='ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/v3',
          prefix='ghcnm',
          reading='tmax',
          date='latest',
          adj='qcu',
          subdir='./data',
          untar.function=my.untar) {
  file.name<-get.file.name(prefix,reading,date,adj)
  source.file.name<-file.path(data.path,file.name)
  dest.file<-file.path(subdir,file.name)
  download.file(source.file.name,dest=dest.file)
  return (untar.function(dest.file,list=TRUE))
}

fread.data<-function(file.name) {
  raw<-fread(file.name,sep='\t',header=FALSE)
  ids<-substr(raw$V1,1,11)
  year<-as.integer(substr(raw$V1,12,15))
  element<-substr(raw$V1,16,19)
  result<-cbind(raw,ids,year,element)
  result$V1<-NULL
  columns<-c('ID','YEAR','ELEMENT')
  for (i in 1:12) {
    pos<-8*i+12
    value.as.integer<-as.numeric(substring(raw$V1,pos,pos+4))
    value<-unlist(lapply(value.as.integer,function(v) {if (v==-9999) return(as.numeric('NA')) else return(v/100)}))
    dmflag<-substring(raw$V1,pos+5,pos+5)
    qcflag<-substring(raw$V1,pos+6,pos+6)
    dsflag<-substring(raw$V1,pos+7,pos+7)
    result<-cbind(result,value,dmflag,qcflag,dsflag)
    columns<-c(columns,
               sprintf('VALUE%d',i),
               sprintf('DMFLAG%d',i),
               sprintf('QCFLAG%d',i),
               sprintf('DSFLAG%d',i))
  }
  colnames(result)<-columns
  return (result)
}


fread.index<-function(file.name) {
  raw<-fread(file.name,sep='\t',header=FALSE)
  ids<-substr(raw$V1,1,11)
  latitude<-as.numeric(substr(raw$V1,13,20))
  longitude<-as.numeric(substr(raw$V1,22,30))
  stnelev<-as.numeric(substr(raw$V1,32,37))
  names<-substr(raw$V1,39,68)
  grelev<-as.integer(substr(raw$V1,70,73))
  popcls<-substr(raw$V1,74,74)
  popsiz<-as.integer(substr(raw$V1,75,79))
  topo<-substr(raw$V1,80,81)
  stveg<-substr(raw$V1,82,83)
  stloc<-substr(raw$V1,84,85)
  ocndis<-as.integer(substr(raw$V1,86,87))
  airstn<-substr(raw$V1,89,90)
  towndis<-as.integer(substr(raw$V1,89,90))
  grveg<-substr(raw$V1,91,106)
  popcss<-substr(raw$V1,107,107)
  result<-cbind(raw,ids,latitude,longitude, stnelev,names,grelev,popcls,popsiz,
                topo,stveg,stloc,ocndis,airstn,towndis,grveg,popcss)
  result$V1<-NULL
  colnames(result)<-c(
    "ID", "LATITUDE", "LONGITUDE", "STNELEV", "NAME", "GRELEV", "POPCLS", "POPSIZ",
    "TOPO", "STVEG", "STLOC", "OCNDIS", "AIRSTN", "TOWNDIS", "GRVEG", "POPCSS"
  )
  return (result)
}