GenomeBaser
===========

.. image:: https://landscape.io/github/mscook/GenomeBaser/master/landscape.png
   :target: https://landscape.io/github/mscook/GenomeBaser/master

.. image:: http://gitshields.com/v2/drone/github.com/mscook/GenomeBaser/brightgreen-red.png
  :target: https://drone.io/github.com/mscook/GenomeBaser

.. image:: https://readthedocs.org/projects/genomebaser/badge/?version=latest
    :target: https://readthedocs.org/projects/genomebaser/?badge=latest

.. image:: https://gemnasium.com/mscook/GenomeBaser.svg
    :target: https://gemnasium.com/mscook/GenomeBaser

|

A tool to manage complete (bacterial) genomes from the NCBI.

Most current release is 0.1.2_ (download).


Why?
----

GenomeBaser:
    1) Encourages best practice (uses rsync -> only update what's needed),
    2) Despises filenames that aren't easy to understand (symlinks from 
       RefSeq based filename to Genus_species_strain.gbk),
    3) Gives you what you will (probably) want in the future (provides both .gbk 
       and .fna. Generates PROKKA databases), and
    4) Understands important differences (partitions complete chromosome and 
       complete plasmid into separate directories).


Installation
------------

Something like::

    $ pip install GenomeBaser

Alternatively::

    $ wget https://github.com/mscook/GenomeBaser/archive/v0.1.2.tar.gz
    $ tar -zxvf v0.1.2.tar.gz
    $ cd v0.1.2
    $ # May need sudo/root, BUT...
    $ python setup.py install


Usage
-----

Something like::

    $ GenomeBaser --help
        Usage: GenomeBaser [OPTIONS] GENUS SPECIES OUT_DATABASE_LOCATION

        GenomeBaser is tool to manage complete (bacterial) genomes from the NCBI.

        Example usage:

              $ GenomeBaser Klebsiella pneumoniae ~/dbs

              $ # (wait a few months)...

              $ GenomeBaser Klebsiella pneumoniae ~/dbs

        By Mitchell Stanton-Cook (m.stantoncook@gmail.com)

        **More info at:** https://github.com/mscook/GenomeBaser

        Options:
          --check_deps / --no-check_deps  Check that non-python dependencies exist
          --help                          Show this message and exit.



.. _0.1.2: https://github.com/mscook/GenomeBaser/archive/v0.1.2.tar.gz
