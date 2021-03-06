# dna-proto workflow (Snakemake)

<img src="https://divingintogeneticsandgenomics.rbind.io/img/snakemake.png" alt="Girl in a jacket" width="200" height="150">  

This workflow is for analysing genome re-sequencing experiments. It features 2 modes. The **de-novo** mode is used to confirm sample relationships from the raw sequencing reads with [kwip](https://github.com/kdmurray91/kWIP) and [mash](https://github.com/marbl/Mash). The **varcall** mode performs read alignments to one or several reference genomes followed by variant detection. Read alignments can be performed with [bwa](http://bio-bwa.sourceforge.net/bwa.shtml) and/or [NextGenMap](https://github.com/Cibiv/NextGenMap/wiki) and  variant calling with [Freebayes](https://github.com/ekg/freebayes) and/or [bcftools mpileup](https://samtools.github.io/bcftools/howtos/variant-calling.html). These tools are currently [the best performing tools](https://link.springer.com/article/10.1186/s12859-020-03704-1) when re-sequencing large plant genomes. Between read alignment and variant calling, PCR duplicates are flagged with [samtools markdup](http://www.htslib.org/doc/samtools-markdup.html) and indels realigned with [abra2](https://github.com/mozack/abra2).
If a genome annotation is available, variants are annotated with [snpEff](https://pcingola.github.io/SnpEff/).

## Authors

*   Norman Warthmann
*   Marcos Conde
*   Kevin Murray*

*Core functionality of this workflow is based on  [PaneucalyptShortReads](https://github.com/kdmurray91/PaneucalyptShortReads)


## Usage

1.  Create a new github repository in your github account using this workflow [as a template](https://help.github.com/en/articles/creating-a-repository-from-a-template).
2.  [Clone](https://help.github.com/en/articles/cloning-a-repository) your newly created repository to your local system where you want to perform the analysis.
3.  **Setup** the software dependencies
4.  **Configure** the workflow for your needs and input files
5.  **Run** the workflow
6.  [**Archive** your workflow](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#sustainable-and-reproducible-archiving) for documenting your work and easy reproduction.

Some pointers for **setup**, **configuring** and **running** the workflow are below, for details please consult the documentation.

----

## [Setup](https://snakemake.readthedocs.io/en/stable/tutorial/setup.html)

An easy way to setup the dependencies is conda.

**Get the Miniconda Python 3 distribution:**

```
$ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh
```

**Create an environment with the required software:**

> NOTE: conda's enviroment name in these examples is `dna-proto`.

```
$ conda env create --name dna-proto --file envs/condaenv.yml
```

**Activate the environment:**

```
$ conda activate dna-proto
```

Additional useful conda commands are [here](https://gist.github.com/mv-lab/62318ff0023bd626f1e05ed9c0155fd5).

<br>

----

## Check config and metadata

We provide scripts to list metadata and configuration parameters in ```utils/```.

```
python utils/check_metadata.py
python utils/check_config.py
```

<br>

## Visualising the workflow
You can check the workflow in graphical form by printing the so-called DAG.

```
snakemake --dag -npr -j -1 | dot -Tsvg > dag.svg
eog dag.svg
```

## Pretending a run of the workflow
Prior to running the workflow, pretend a run and confirm it will do what is intended.

```
snakemake  -npr
```

## Data

Main directory content:

```
.
├── envs
├── genomes_and_annotations
├── metadata
├── output
├── rules
├── scripts
├── utils
├── config.yml
├── Snakefile
├── snpEff.config

```
> NOTE: the ```output``` directory and some files in the ```metadata``` directory are/will be generated by the workflow.

You will need to configure the workflow for your specific project. For details see the documentation. Below files and directories will need editing:

-   **Snakefile**
-   **genomes_and_annotations/**
-   **metadata/**
-   **config.yml**
-   **snpEff.config**

You can download example data for testing the workflow. [click here to download](https://drive.google.com/drive/folders/1kpJsghU-jNTSKC9uEB9khos390lZNROr?usp=sharing)

--
