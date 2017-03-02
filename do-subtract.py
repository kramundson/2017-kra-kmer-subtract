#! /usr/bin/env python3
import khmer, khmer.utils
import screed
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('A')
    p.add_argument('B')
    p.add_argument('C')
    p.add_argument('output')
    p.add_argument('-k', '--ksize', default=31)
    args = p.parse_args()

    # for potato, would suggest changing 1e6 to 4e9
    a_table = khmer.Nodetable(args.ksize, 1e6, 4) # 1e6 needs to be changed
    b_table = khmer.Nodetable(args.ksize, 1e6, 4)

    b_table.consume_seqfile(args.B)

    n_hashes_loaded = 0
    for record in khmer.utils.clean_input_reads(screed.open(args.A)):
        for hash in a_table.get_kmer_hashes(record.cleaned_seq):
            if not b_table.get(hash):
                a_table.add(hash)
                n_hashes_loaded += 1

    print('loaded {} k-mers in A but not in B'.format(n_hashes_loaded))
    # at this point, a_table contains A - B


    out_fp = open(args.output, 'w')
    n_read = 0
    n_written = 0
    
    for record in khmer.utils.clean_input_reads(screed.open(args.C)):
        n_read += 1
        for hash in a_table.get_kmer_hashes(record.cleaned_seq):
            if a_table.get(hash):
                khmer.utils.write_record(record, out_fp)
                n_written += 1
                break

    print('wrote {} of {} records to {}'.format(n_written, n_read,
                                                args.output))

if __name__ == '__main__':
    main()
