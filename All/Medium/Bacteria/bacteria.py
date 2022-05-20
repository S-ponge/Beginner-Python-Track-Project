class Bacteria:
    nucleotides = {"A": "T", "T": "A", "C": "G", "G": "C"}

    def __init__(self, _lines):
        self.plasmid = _lines[0]
        self.cut_plasmid_strand = None
        self.plasmid_restriction_site = _lines[1]
        self.gfp_strand = _lines[2]
        self.cut_gfp_strand = None
        self.gfp_restriction_sites = _lines[3].split()
        self.complementary_seq = None

    def get_complementary_seq(self):
        return f'{self.plasmid}\n{self.complementary_seq}'

    def set_complementary_seq(self, sequence):
        seq = ""
        for char in sequence:
            seq += self.nucleotides[char]
        return seq

    def cut_strands(self):
        self.find_restricted_sites(self.plasmid, self.plasmid_restriction_site, is_plasmid=True)
        self.find_restricted_sites(self.gfp_strand, self.gfp_restriction_sites, is_GFP=True)

    def find_restricted_sites(self, strand, r_s, is_GFP=None, is_plasmid=None):
        if is_plasmid:
            index = strand.index(r_s) + 1
            self.cut_plasmid_strand = strand[:index] + " " + strand[index:]
        elif is_GFP:
            start_index = strand.index(r_s[0]) + 1
            end_index = strand.rindex(r_s[1]) + 1
            self.cut_gfp_strand = strand[start_index:end_index]


    def perform_ligation(self):
        first = self.cut_plasmid_strand.replace(" ", self.cut_gfp_strand)
        self.complementary_seq = self.set_complementary_seq(first)
        return f'{first}\n{self.complementary_seq}'

file_name = input()
file = open(file_name, "r")
lines = file.readlines()
lines = [line.rstrip("\n") for line in lines]
file.close()
bacteria = Bacteria(lines)
bacteria.cut_strands()
print(bacteria.perform_ligation())


# def find_restriction_sites(self):
#     restrictions = {"original": "", "complementary": ""}
#     o_index = 0
#     for site in restrictions:
#         if site == "original":
#             o_index = self.sequence.index(self.front_restrict_site)
#             end_index = self.sequence.rindex(self.end_restrict_site)
#             restrictions[site] = self.sequence[o_index + 1:end_index + 1]
#         else:
#             front = self.set_complementary_seq(self.front_restrict_site)
#             end = self.set_complementary_seq(self.end_restrict_site)
#             c_index = self.complementary_seq.index(front)
#             end_index = self.complementary_seq.rindex(end)
#             restrictions[site] = self.complementary_seq[c_index + 5:end_index + 5]
#     return f'{restrictions["original"]}\n{restrictions["complementary"]}'



