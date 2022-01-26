class Sequence:
    def __init__(self, lines):
        self.name = lines[0].strip()[1:]
        self.bases = "".join([x.strip() for x in lines[1:]]).upper()

    def __str__(self):
        return self.name + ": " + self.bases[:20] + "..."

    def __repr__(self):
        return self.__str__()


class Read(Sequence):
    def get_seed(self, seedlength):
        return self.bases[:seedlength]

    def replace_kmers(self, replacements):
        pass

class Reference(Sequence):
    def __init__(self, lines):
        self.kmers = None
        super().__init__(lines)

    def calculate_kmers(self, kmersize):
        self.kmers = {}
        for pos in range(0, len(self.bases) - kmersize + 1):
            kmer = self.bases[pos:(pos + kmersize)]
            if kmer not in self.kmers:
                self.kmers[kmer] = []
            self.kmers[kmer] += [pos]

    def get_kmer_positions(self, kmer):
        if self.kmers is None or len(next(iter(self.kmers))) != len(kmer):
            self.calculate_kmers(len(kmer))
        if kmer not in self.kmers:
            return []
        return self.kmers[kmer]

    def count_mismatches(self, read, position):
        mismatches = 0
        for pos in range(position, position+len(read.bases)):
            if pos >= len(self.bases):
                break
            if read.bases[pos-position] != self.bases[pos]:
                mismatches += 1
        # Count every base of the read that goes out past the end of the reference as a mismatch
        mismatches += position+len(read.bases)-pos-1
        return mismatches


class Mapping:
    def __init__(self, reference):
        self.reference = reference
        self.reads = {}

    def add_read(self, read, position):
        if position not in self.reads:
            self.reads[position] = []
        self.reads[position] += [read]

    def get_reads_at_position(self, position):
        if position not in self.reads:
            return []
        return self.reads[position]

    def get_pileup(self):
        readlist = dict()
        pileup = []
        for position in range(0, len(self.reference.bases)):
            refbase = self.reference.bases[position]
            bases = []
            todel = []
            for read in self.get_reads_at_position(position):
                readlist[read] = position
            for read in readlist:
                if (position - readlist[read]) >= len(read.bases) :
                    todel += [read]
                    continue
                base = read.bases[position - readlist[read]]
                if base == refbase:
                    bases += ["."]
                else:
                    bases += [base]
            for read in todel:
                readlist.pop(read)
            pileup += [[position+1, refbase, len(bases), "".join(bases)]]
        return pileup

    def __str__(self):
        res = ["Mapping to " + self.reference.name]
        for pos in self.reads:
            res += ["  " + str(len(self.reads[pos])) + " reads mapping at " + str(pos)]
        return "\n".join(res)


class MappingWriter:
    def __init__(self, mapping):
        self.mapping = mapping

    def write_sam(self, filename):
        f = open(filename, "w")
        refname = self.mapping.reference.name.split(" ")[0]
        f.write("@SQ\tSN:" + refname + "\tLN:" + str(len(self.mapping.reference.bases)) + "\n")
        for pos in range(0, len(self.mapping.reference.bases)):
            for read in self.mapping.get_reads_at_position(pos):
                f.write("\t".join([read.name, "0", refname, str(pos+1), "255",
                                   str(len(read.bases))+"M", "*", "0", "0", read.bases, "*"]))
                f.write("\n")
        f.close()

    def write_pileup(self, filename):
        f = open(filename, "w")
        refname = self.mapping.reference.name.split(" ")[0]
        pileup = self.mapping.get_pileup()
        for line in pileup:
            f.write(refname)
            f.write("\t")
            f.write("\t".join([str(x) for x in line]))
            f.write("\n")
        f.close()

class ReadPolisher:
    def __init__(self, kmerlen):
        pass

    def add_read(self, readseq):
        pass

    def get_replacements(self, minfreq):
        pass

def read_fasta(fastafile, klassname):
    klass = globals()[klassname]
    f = open(fastafile, "r")
    readlines = []
    reads = []
    for line in f:
        if line[0] == '>' and len(readlines) != 0:
            reads += [klass(readlines)]
            readlines = []
        readlines += [line]
    reads += [klass(readlines)]
    f.close()
    return reads


def map_reads(reads, reference, kmersize, max_mismatches):
    mapping = Mapping(reference)
    reference.calculate_kmers(kmersize)
    for read in reads:
        seed = read.get_seed(kmersize)
        seed_positions = reference.get_kmer_positions(seed)
        for position in seed_positions:
            mismatches = reference.count_mismatches(read, position)
            if mismatches < max_mismatches:
                mapping.add_read(read, position)
    return mapping


def main():
    reads = read_fasta("data/patient1.fasta", Read.__name__)
    reference = read_fasta("data/rpoB.fasta", Reference.__name__)[0]
    mapping = map_reads(reads, reference, 8, 2)
    writer = MappingWriter(mapping)
    writer.write_sam("data/mapping_p1_uncorrected.sam")
    polisher = ReadPolisher(15)
    for read in reads:
        polisher.add_read(read.bases)
    replacements = polisher.get_replacements(10)
    nrep = 0
    for read in reads:
        nrep += 1
        if nrep % 1000 == 0:
            print(str(nrep) + "/" + str(len(reads)))
        read.replace_kmers(replacements)
    mapping = map_reads(reads, reference, 8, 2)
    writer = MappingWriter(mapping)
    writer.write_sam("data/mapping_p1_corrected.sam")


if __name__ == "__main__":
    main()
