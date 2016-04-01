import math
import time
import multiprocessing as mul
from multiprocessing import Manager
import csv

class onedocument:
    def __init__(self,document,length):
        self.document=document;
        self.length=length;

class simMatrix:
    manager=Manager()
    sim=manager.list()
    @staticmethod
    def init_sim(doc_len):
        if len(simMatrix.sim) == 0:
            simMatrix.sim=simMatrix.manager.list([([0] * doc_len) for i in range(doc_len)])


class tfidf:
    def __init__(self):
        self.docs=[];
        self.df={};
        self.lntf=[0]*4000
        for i in range(1,len(self.lntf)):
            self.lntf[i]=math.log(i)
        self.tf=[0]*1000
        for i in range(1,len(self.tf)):
            self.tf[i]=1+math.log(1+self.lntf[i])

    def setstopword(self,stopwordfilename):
        file = open(stopwordfilename)
        lines=file.readlines()
        file.close()
        self.stopword=set()
        for word in lines:
            word = word.split()[0]
            if not word in self.stopword:
                self.stopword.add(word)

    def readfile(self,filename):
        file = open(filename)
        lines=file.readlines()
        file.close()
        doc={}
        wordlen=0
        length=0
        for oneline in lines:
            words=oneline.split()[1:]
            wordlen+=len(words)
            length+=len(words)
            if(len(words) == 0):
                adoc=onedocument(doc,length)
                self.docs.append(adoc)

                for word in doc:
                    if not word in self.df:
                        self.df[word]=1;
                    else:
                        self.df[word]+=1;

                doc={}
                length=0
            else:
                for curword in words:
                    curword = curword.split("/")[0]

                    if not curword in self.stopword:
                        if curword in doc.keys():
                            doc[curword]+=1;
                        else:
                            doc[curword]=1;
        if len(doc) != 0:
            adoc=onedocument(doc,length)
            self.docs.append(adoc)
            for word in doc:
                    if not word in self.df:
                        self.df[word]=1;
                    else:
                        self.df[word]+=1;

        self.totalword=wordlen

    def calsims(self):
        print('cal sims')
        doc_len=len(self.docs)
        print("doc len: ",doc_len)
        self.doc_len=doc_len
        self.nplusone=doc_len+1
        self.ln_lplusone=self.lntf[self.nplusone]
        self.avdl=self.totalword/doc_len
        print("avdl : %s" % self.avdl)
        # simMatrix.sim= [([0] * doc_len) for i in range(doc_len)]
        # simMatrix.sim= [([0] * doc_len) for i in range(doc_len)]
        simMatrix.init_sim(doc_len)
        pool_num=4
        print("proceses : %s" % pool_num)
        pool=mul.Pool(pool_num)
        pool.map_async(self.cal_i_with_others,range(0,doc_len))
        pool.close()
        pool.join()

    def cal_i_with_others(self,i):
        len_i=self.docs[i].length
        denominator=(1-0.2)+0.2*len_i/self.avdl
        cur_list=[]
        for j in range(0,i+1):
            cur_list.append(0)
        for j in range(i+1,self.doc_len):
            len_j=self.docs[j].length
            if(len_i>len_j):
                cur_list.append(self.cal_two_document(denominator,self.docs[j].document,self.docs[i].document))
                    # simMatrix.sim[i][j]=self.cal_two_document(denominator,self.docs[j].document,self.docs[i].document)
            else:
                cur_list.append(self.cal_two_document(denominator,self.docs[i].document,self.docs[j].document))
                    # simMatrix.sim[i][j]=self.cal_two_document(denominator,self.docs[i].document,self.docs[j].document)
        simMatrix.sim[i]=cur_list

    def cal_two_document(self,denominator,doca,docb):
        sim=0
        for word in doca:
            if word in docb:
                numerator=self.tf[docb[word]]
                cur_ifidf=numerator*doca[word]*(self.ln_lplusone-self.lntf[self.df[word]])
                sim+=cur_ifidf
        return sim/denominator


class calc:
    @staticmethod
    def calc_time():
        start_time=time.time();
        a = tfidf()
        a.setstopword('stopword')
        a.readfile('text.txt')
        mid_time=time.time();
        a.calsims()
        fout=open("result.csv","w",newline="")
        writer=csv.writer(fout)
        writer.writerows(simMatrix.sim)
        fout.close()
        stop_time=time.time();
        print("calculation time: %s" % (stop_time-mid_time))
        print("total time: %s" % (stop_time-start_time))


calc.calc_time()

