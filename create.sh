~/dev/nullgraph/make-random-genome.py -l 10000 -s 1 --name=A > a.fasta
~/dev/nullgraph/make-random-genome.py -l 10000 -s 2 --name=B > b.fasta

~/dev/nullgraph/make-reads.py -r 100 -C 10 -e .01 a.fasta > a.reads.fa
~/dev/nullgraph/make-reads.py -r 100 -C 10 -e .01 b.fasta > b.reads.fa

echo '>c' > c.fasta
cat a.fasta b.fasta | grep -v ^'>' >> c.fasta

~/dev/nullgraph/make-reads.py -r 100 -C 10 -e .01 c.fasta > c.reads.fa

