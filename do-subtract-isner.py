#! /usr/bin/python
import argparse, os, sys
sys.path.insert(0,'./khmerEnv/lib/python2.7/site-packages')
import khmer, khmer.utils
import screed

def fastqGrab():

    '''Return *.fastq files in directory as a list.
    For potato, can leave parents as .fastq files
    as a control'''
    
    li = os.listdir(os.getcwd())
    todo = list(filter(lambda x: x[-6:] == '.fastq', li))
    return(todo)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('A')
    p.add_argument('B')
    #p.add_argument('C')
    p.add_argument('output')
    p.add_argument('-k', '--ksize', default=31, type=int)
    args = p.parse_args()

    # for potato, would suggest changing 1e6 to 4e9. Only matters for A-B hash.
    a_table = khmer.Nodetable(args.ksize, 10e9, 4)
    b_table = khmer.Nodetable(args.ksize, 10e9, 4)
    b_table.consume_seqfile(args.B)

    n_hashes_loaded = 0
    for record in khmer.utils.clean_input_reads(screed.open(args.A)):
        for hash in a_table.get_kmer_hashes(record.cleaned_seq):
            if not b_table.get(hash):
                a_table.add(hash)
                n_hashes_loaded += 1

    print('loaded {} k-mers in A but not in B'.format(n_hashes_loaded))
    # at this point, a_table contains A - B
    
    out_table = open(args.output, 'w')
    head = 'sample\ttotal-read\thap-kmer-read\ttotal-kmer\tkmer-hits\n'
    out_line = '' # one string to rule them all
    
    for fastq in fastqGrab():
        print('Now querying {}'.format(fastq))
        hitcount = 0 # initialize hitcount
        hashcount = 0 # initialize hashcount
        out_fp = open(fastq+'.subset', 'w')
        n_read = 0
        n_written = 0
        
        for record in khmer.utils.clean_input_reads(screed.open(fastq)):
            n_read += 1
            match = 0 # adopt O state for no hits in read, change to 1 when match in read
            
            for hash in a_table.get_kmer_hashes(record.cleaned_seq):
                hashcount += 1
                if a_table.get(hash):
                    match = 1 # swtich to state "match"
                    hitcount += 1 # tally k-mer hit
                    
            if match == 1: # write to file if switch tripped
                khmer.utils.write_record(record, out_fp)
                n_written += 1
                #break
                
        print('wrote {} of {} records for {}'.format(n_written, n_read,
                                                fastq))
        out_line += fastq + '\t'+ str(n_read) + '\t' + str(n_written) + '\t' + str(hashcount) + '\t' + str(hitcount) + '\n'
        
    out_table.write(head+out_line)

if __name__ == '__main__':
    main()
