#!/usr/bin/perl
# Kirk Amundson
# AtoQ.pl
# 3 October 2016
# Accept fasta formatted file at command line, write to converted fastq file

# USAGE: program.pl input.fasta

# interpret file provided at command line
my $fasta = shift @ARGV;
my @fastq = split(/\./, $fasta);
my $fastq = join(".", @fastq[0..1]) . '.fastq';

# open filehandle and process
open FASTA, "<", "$fasta" or die "Usage: program.pl input.fasta: $!";
open FASTQ, ">", "$fastq" or die "problem opening $fastq\n";

while (my $line = <FASTA>) {
    $linecount++;
    if ($linecount%2 == 1) {
        $line =~ s/^>/@/g;
        $head = $line;
        $head =~ tr/@/+/;
        print FASTQ $line;
    }
    elsif ($linecount%2 == 0) {
        print FASTQ $line;
        print FASTQ $head;
        print (FASTQ "X" x (length($line)-1) . "\n");
    }
}