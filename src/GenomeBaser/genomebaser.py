#!/usr/bin/env python

"""
Genomebaser is a tool to manage complete genomes from the NCBI
"""

__title__ = 'GenomeBaser'
__version__ = '0.1.2'
__description__ = "GenomeBaser manages complete (bacterial) genomes from NCBI"
__author__ = 'Mitchell Stanton-Cook'
__author_email__ = 'm.stantoncook@gmail.com'
__url__ = 'http://github.com/mscook/GenomeBaser'
__license__ = 'ECL 2.0'

import os
import re
import glob
import sys
import subprocess

from Bio import SeqIO
import click


def check_for_deps():
    """
    Check if 3rd party dependencies (non-python) exist

    Requires:
        * rsysnc
        * prokka-genbank_to_fasta_db
        * cd-hit
        * makeblastdb
    """
    reqs = ["rsync", "prokka-genbank_to_fasta_db", "cd-hit", "makeblastdb"]
    for e in reqs:
        output = subprocess.Popen(["which", e],
                                  stdout=subprocess.PIPE).communicate()[0]
        if output.split("/")[-1].strip() != e:
            print "Misisng %s. Please install. Exiting." % (e)
            sys.exit()


def fetch_genomes(target_genus_species, db_base=None):
    """
    Use rsync to manage periodic updates

    Examples:

    >>> fetch_genomes("Escherichia coli")
    >>>
    >>> fetch_genomes("Klebsiella pneumoniae", "/home/me/dbs/")

    :param target_genus_species: the genus species as a string
                                 (space delimited)

    :returns: the database location
    """
    working_dir = os.getcwd()
    if db_base is not None:
        os.chdir(db_base)
    target_genus_species = target_genus_species.replace(" ", "_")
    if not os.path.exists(target_genus_species):
        os.mkdir(target_genus_species)
    os.chdir(target_genus_species)
    cmd = ("rsync -av ftp.ncbi.nlm.nih.gov::genomes/Bacteria/"
           "%s_*/*.gbk .") % (target_genus_species)
    db_loc = os.getcwd()
    os.system(cmd)
    os.chdir(working_dir)
    return db_loc


def genbank_to_fasta(db_loc):
    """
    Converts GenBank to fasta while naming using the given in the DEFINITION

    Examples:

    >>> genbank_to_fasta("/home/mscook/dbs/Klebsiella_pneumoniae"

    :param db_loc: the fullpath as a sting to the database location (genus
                   species inclusive)

    :returns: a list of the output fasta files
    """
    fasta_files = []
    tmp_file = "tmp.gbk"
    working_dir = os.getcwd()
    os.chdir(db_loc)
    infs = glob.glob("*.gbk")
    for inf in infs:
        cmd = "grep -v 'CONTIG      join' "+inf+" > "+tmp_file
        os.system(cmd)
        os.rename(tmp_file, inf)
        for seq_record in SeqIO.parse(inf, "genbank"):
            out_fa = re.sub(r'\W+', ' ', seq_record.description
                            ).replace(' ', '_')
            if out_fa.endswith('_'):
                out_fa = out_fa[:-1]+".fna"
            else:
                out_fa = out_fa+".fna"
            SeqIO.write(seq_record, out_fa, "fasta")
            fasta_files.append(out_fa)
            dest = out_fa.replace(".fna", ".gbk")
            if not os.path.lexists(dest):
                os.symlink(inf, dest)
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
    os.chdir(working_dir)
    return fasta_files


def partition_genomes(db_loc, fasta_files):
    """
    Separate complete genomes from plasmids

    ..warning:: this partitions on the complete_sequence (plasmid) vs
                complete_genome (genome) in filename assumption (in
                DEFINITION) line

    :param db_loc: the fullpath as a sting to the database location (genus
                   species inclusive)

    :param fasta_files: a list of fasta files

    :returns: a list of DEFINITION format named GenBank files
    """
    plasmid, genome = [], []
    working_dir = os.getcwd()
    os.chdir(db_loc)
    for e in fasta_files:
        if e.find("complete_sequence") != -1:
            plasmid.append(e)
        elif e.find("complete_genome") != -1:
            genome.append(e)
        elif e.find("_genome") != -1:
            genome.append(e)
        else:
            print "Could not classify %s" % (e)
            print "Continuing..."
    if not os.path.exists("plasmid"):
        os.mkdir("plasmid")
    os.chdir("plasmid")
    for e in plasmid:
        if not os.path.lexists(e):
            os.symlink("../"+e, e)
    os.chdir("../")
    if not os.path.exists("genome"):
        os.mkdir("genome")
    os.chdir("genome")
    for e in genome:
        if not os.path.lexists(e):
            os.symlink("../"+e, e)
    os.chdir("../")
    os.chdir(working_dir)
    return genome


def make_prokka(db_loc, genbank_files, target_genus_species):
    """
    Make a prokka database of the complete genomes

    :param db_loc: the fullpath as a sting to the database location (genus
                   species inclusive)

    :param genbank_files: a list of GenBank files

    :param target_genus_species: the genus species as a string
                                 (space delimited)
    """
    working_dir = os.getcwd()
    os.chdir(db_loc)
    target = target_genus_species.split(" ")[0]
    if not os.path.exists("prokka"):
        os.mkdir("prokka")
    prokka_cmd = ("prokka-genbank_to_fasta_db %s --idtag=locus_tag "
                  "> prokka/%s.faa") % (' '.join(genbank_files), target)
    os.system(prokka_cmd.replace(".fna", ".gbk"))
    os.chdir("prokka")
    cd_hit_cmd = ("cd-hit -i %s.faa -o %s -T 0 "
                  "-M 0 -g 1 -s 0.8 -c 0.9") % (target, target)
    os.system(cd_hit_cmd)
    blast_cmd = "makeblastdb -dbtype prot -in %s" % (target)
    os.system(blast_cmd)
    os.chdir("../")
    os.chdir(working_dir)


@click.command()
@click.option('--check_deps/--no-check_deps', default=True,
              help='Check that non-python dependencies exist')
@click.argument("genus")
@click.argument("species")
@click.argument('out_database_location', type=click.Path(exists=True))
def main(check_deps, genus, species, out_database_location):
    """
    GenomeBaser is tool to manage complete (bacterial) genomes from the NCBI.

    Example usage:

        $ GenomeBaser.py Klebsiella pneumoniae ~/dbs

        $ # (wait a few months)...

        $ GenomeBaser Klebsiella pneumoniae ~/dbs

    By Mitchell Stanton-Cook (m.stantoncook@gmail.com)

    **More info at:** https://github.com/mscook/GenomeBaser
    """
    if check_deps:
        print "Checking for 3rd party dependencies"
        check_for_deps()
    genus = genus[0].upper()+genus[1:]
    gs = genus+" "+species
    loc = fetch_genomes(gs, out_database_location)
    fas = genbank_to_fasta(loc)
    genbanks = partition_genomes(loc, fas)
    make_prokka(loc, genbanks, gs)


if __name__ == '__main__':
        main()
