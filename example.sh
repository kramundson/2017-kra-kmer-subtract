# should return half of c
./do-subtract.py  a.reads.fa b.reads.fa c.reads.fa output.fa

# should return nothing because you're asking for b-b
./do-subtract.py  b.reads.fa b.reads.fa c.reads.fa output.fa
