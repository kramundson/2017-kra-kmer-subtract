# How to set up khmer in a virtual environment on Isner. Sudo not needed.

# Summary of steps:
# 1. Build a python2.7 virtualenv
# 2. Install latest version of khmer and screed in virtualenv
# 3. Set up and run tests

# 1. Build virtualenv
python2.7 -m virtualenv khmerEnv
source khmerEnv/bin/activate

# 2. Install latest khmer screed
pip install -U pip setuptools
pip install https://github.com/dib-lab/khmer/archive/master.zip
pip install https://github.com/dib-lab/screed/archive/master.zip

# 3. Build test files and run test
cat a.reads.fa b.reads.fa >> ab.reads.fa

for i in *.fa
do
	perl AtoQ.pl $i
done

python do-subtract-isner.py a.reads.fastq b.reads.fastq out.test

###EXAMPLE OUTPUT###
