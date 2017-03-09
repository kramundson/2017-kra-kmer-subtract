# Why 1034 reads returned instead of 1000 from original CTB sample?

# should return half of c, but doesn't
./do-subtract.py  a.reads.fa b.reads.fa c.reads.fa output.fa

# should return nothing because you're asking for b-b
./do-subtract.py  b.reads.fa b.reads.fa c.reads.fa output.fa

# It's how we're sampling the reads! This returns half of AB as expected:
cat a.reads.fa b.reads.fa > ab.reads.fa
./do-subtract.py a.reads.fa b.reads.fa ab.reads.fa local.output.fa
