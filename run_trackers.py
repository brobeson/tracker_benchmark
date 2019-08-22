import getopt
import sys
import os

import numpy as np
from PIL import Image
import config
import scripts.butil.seq_config
import scripts.butil.load_results
import scripts.butil.eval_results
import scripts.bscripts.run_dmdnet
from scripts.model.result import Result


def main(argv):
    
    trackers = os.listdir(config.TRACKER_SRC)
    evalTypes = ['OPE', 'SRE', 'TRE']
    loadSeqs = 'TB50'
    seqs = []
    try:
        opts, args = getopt.getopt(argv, "ht:e:s:",["tracker=","evaltype="
            ,"sequence="])
    except getopt.GetoptError:
        print('usage : run_trackers.py -t <trackers> -s <sequences>' \
            + '-e <evaltypes>')
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print('usage : run_trackers.py -t <trackers> -s <sequences>' \
                + '-e <evaltypes>')
            sys.exit(0)
        elif opt in ("-t", "--tracker"):
            trackers = [x.strip() for x in arg.split(',')]
            # trackers = [arg]
        elif opt in ("-s", "--sequence"):
            loadSeqs = arg
            if loadSeqs != 'All' and loadSeqs != 'all' and \
                loadSeqs != 'tb50' and loadSeqs != 'tb100' and \
                loadSeqs != 'cvpr13':
                loadSeqs = [x.strip() for x in arg.split(',')]
        elif opt in ("-e", "--evaltype"):
            evalTypes = [x.strip() for x in arg.split(',')]
            # evalTypes = [arg]

    if config.SETUP_SEQ:
        print('Setup sequences ...')
        scripts.butil.seq_config.setup_seqs(loadSeqs)
    testname = "foo"  #input("Input Test name : ")
    print(f'Starting benchmark for {len(trackers)} trackers, evalTypes : {evalTypes}')
    #print 'Starting benchmark for {0} trackers, evalTypes : {1}'.format(len(trackers), evalTypes)
    for evalType in evalTypes:
        seqNames = scripts.butil.seq_config.get_seq_names(loadSeqs)
        seqs = scripts.butil.seq_config.load_seq_configs(seqNames)
        trackerResults = run_trackers(
            trackers, seqs, evalType, config.shiftTypeSet)
        for tracker in trackers:
            results = trackerResults[tracker]
            if len(results) > 0:
                evalResults, attrList = scripts.butil.eval_results.calc_result(tracker,
                    seqs, results, evalType)
                print(f"Result of Sequences\t -- '{tracker}'")
                #print "Result of Sequences\t -- '{0}'".format(tracker)
                for seq in seqs:
                    try:
                        print(f'\t\'{seq.name}\' ')
                        #print '\t\'{0}\'{1}'.format(seq.name, " "*(12 - len(seq.name))),
                        #print "\taveCoverage : {0:.3f}%".format(sum(seq.aveCoverage)/len(seq.aveCoverage) * 100),
                        #print "\taveErrCenter : {0:.3f}".format(sum(seq.aveErrCenter)/len(seq.aveErrCenter))
                    except:
                        print('\t\'', seq.name, '\'  ERROR!!')
                        #print '\t\'{0}\'  ERROR!!'.format(seq.name)

                print(f"Result of attributes\t -- '{tracker}'")
                #print "Result of attributes\t -- '{0}'".format(tracker)
                for attr in attrList:
                    print(f"\t\'{attr.name}\'")
                    #print "\t\'{0}\'".format(attr.name),
                    #print "\toverlap : {0:02.1f}%".format(attr.overlap),
                    #print "\tfailures : {0:.1f}".format(attr.error)

                if config.SAVE_RESULT : 
                    scripts.butil.load_results.save_scores(attrList, testname)

def run_trackers(trackers, seqs, evalType, shiftTypeSet):
    tmpRes_path = config.RESULT_SRC.format('tmp/{0}/'.format(evalType))
    if not os.path.exists(tmpRes_path):
        os.makedirs(tmpRes_path)

    numSeq = len(seqs)
    numTrk = len(trackers)

    trackerResults = dict((t,list()) for t in trackers)
    for idxSeq in range(numSeq):
        s = seqs[idxSeq]
        
        subSeqs, subAnno = scripts.butil.seq_config.get_sub_seqs(s, 20.0, evalType)

        for idxTrk in range(len(trackers)):         
            t = trackers[idxTrk]
            if not config.OVERWRITE_RESULT:
                trk_src = os.path.join(config.RESULT_SRC.format(evalType), t)
                result_src = os.path.join(trk_src, s.name+'.json')
                if os.path.exists(result_src):
                    seqResults = scripts.butil.load_results.load_seq_result(evalType, t, s.name)
                    trackerResults[t].append(seqResults)
                    continue
            seqResults = []
            seqLen = len(subSeqs)
            for idx in range(seqLen):
                print(f'{idxTrk + 1}_{t}, {idxSeq + 1}_{s.name}:{idx + 1}/{seqLen} - {evalType}')
                #print '{0}_{1}, {2}_{3}:{4}/{5} - {6}'.format(
                #    idxTrk + 1, t, idxSeq + 1, s.name, idx + 1, seqLen, \
                #    evalType)
                rp = tmpRes_path + '_' + t + '_' + str(idx+1) + '/'
                if config.SAVE_IMAGE and not os.path.exists(rp):
                    os.makedirs(rp)
                subS = subSeqs[idx]
                subS.name = s.name + '_' + str(idx)
                
                move_dir = False
                if os.path.exists(os.path.join(config.TRACKER_SRC, t)):
                    move_dir = True
                    os.chdir(os.path.join(config.TRACKER_SRC, t))
                funcName = "scripts.bscripts.run_dmdnet.run_{0}(subS, rp, config.SAVE_IMAGE)".format(t)
                try:
                    res = eval(funcName)
                except:
                    print(f'failed to execute {t} : {sys.exc_info()}')
                    #print 'failed to execute {0} : {1}'.format(
                    #    t, sys.exc_info())
                    if move_dir:
                        os.chdir(WORKDIR)         
                    break
                if move_dir:
                    os.chdir(WORKDIR)

                if evalType == 'SRE':
                    r = Result(t, s.name, subS.startFrame, subS.endFrame,
                        res['type'], evalType, res['res'], res['fps'], shiftTypeSet[idx])
                else:
                    r = Result(t, s.name, subS.startFrame, subS.endFrame,
                        res['type'], evalType, res['res'], res['fps'], None)
                try: r.tmplsize = res['tmplsize'][0]
                except: pass
                r.refresh_dict()
                seqResults.append(r)
            #end for subseqs
            if config.SAVE_RESULT:
                scripts.butil.load_results.save_seq_result(seqResults)

            trackerResults[t].append(seqResults)
        #end for tracker
    #end for allseqs
    return trackerResults

if __name__ == "__main__":
    main(sys.argv[1:])
