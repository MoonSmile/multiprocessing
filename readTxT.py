import math
import time
import multiprocessing as mul
import csv

class onedocument:
    def __init__(self,document,length):
        self.document=document;
        self.length=length;

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
        self.doc_len=doc_len
        self.nplusone=doc_len+1
        self.ln_lplusone=self.lntf[self.nplusone]
        self.avdl=self.totalword/doc_len
        print("avdl is :%s" % self.avdl)
        self.sim= [([0] * doc_len) for i in range(doc_len)]
        pool=mul.Pool(8)
        pool.map_async(self.cal_i_with_others,range(0,doc_len))
        # for i in range(0,doc_len):
        #     len_i=self.docs[i].length
        #     denominator=(1-0.2)+0.2*len_i/self.avdl
        #     for j in range(i+1,doc_len):
        #         len_j=self.docs[j].length
                # print("i :%s.j:%s, len i: %d ,len j :%d" % (i,j,len_i,len_j))

            # use multiprocessing
            #
            #     if(len_i>len_j):
            #         pool.apply_async(self.cal_sim_i_j,(i,j,denominator,self.docs[j].document,self.docs[i].document,))
            #     else:
            #         pool.apply_async(self.cal_sim_i_j,(i,j,denominator,self.docs[i].document,self.docs[j].document,))

                # if(len_i>len_j):
                #     self.sim[i][j]=self.cal_two_document(denominator,self.docs[j].document,self.docs[i].document)
                # else:
                #     self.sim[i][j]=self.cal_two_document(denominator,self.docs[i].document,self.docs[j].document)
        pool.close()
        pool.join()

    def cal_i_with_others(self,i):
        len_i=self.docs[i].length
        denominator=(1-0.2)+0.2*len_i/self.avdl
        for j in range(i+1,self.doc_len):
            len_j=self.docs[j].length
            if(len_i>len_j):
                    self.sim[i][j]=self.cal_two_document(denominator,self.docs[j].document,self.docs[i].document)
            else:
                    self.sim[i][j]=self.cal_two_document(denominator,self.docs[i].document,self.docs[j].document)
            # print("i :%s.j:%s, len i: %d ,len j :%d sim: %d" % (i,j,len_i,len_j,self.sim[i][j]))


    def cal_sim_i_j(self,i,j,denominator,doci,docj):
        self.sim[i][j]=self.cal_two_document(denominator,doci,docj)
        print("i:%d ,j:%d ,sim :%s " % (i,j,self.sim[i][j]))

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
        writer.writerows(a.sim)
        fout.close()
        stop_time=time.time();
        print("calculation time %s" % (stop_time-mid_time))
        print("total time:%s" % (stop_time-start_time))


calc.calc_time()

