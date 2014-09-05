GenomeBaser
===========

A tool to manage complete (bacterial) genomes from the NCBI.

Most current release is 0.1.1_.


Why?
----

GenomeBaser:
    1) Encourages best practice (uses rsync -> only update what's needed)
    2) Despises filenames that aren't easily understandable (symlinks to 
       RefSeq based filename to  Genus_species_strain.gbk)
    3) Give you what you will probably wan't in the future (provides both .gbk 
       and .fna. Generate PROKKA databases)
    4) Understands important differences (partitions complete chomosome and 
       complete plasmind into separate buckets)


Installation
------------

Something like::

    $ pip install GenomeBaser

Alternatively::

    $ wget https://github.com/mscook/GenomeBaser/archive/v0.1.1.tar.gz
    $ tar -zxvf v0.1.1.tar.gz
    $ cd v0.1.1
    $ # May need sudo/root, BUT...
    $ python setup.py install


Usage
-----

Something like::

    python genomebaser.py 'Pseudomonas aeruginosa' ~/dbs 



.. _0.1.1: https://github.com/mscook/GenomeBaser/archive/v0.1.1.tar.gz
