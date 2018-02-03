class Alignment:
    def __init__(self,title , length, bit_score , correct_procent  , gap, identities, align_lenth, qseq ,hseq,k):
        self.title = title
        self.length = length
        self.bit_score = bit_score
        self.correct_procent = correct_procent
        self.gap = gap
        self.identities = identities
        self.align_length = align_lenth
        self.qseq = qseq
        self.hseq = hseq
        self.k = k

    def __str__(self):
        return "{c} {g} {i}".format(c = self.correct_procent,g = self.gap, i = self.identities)

    def __eq__(self, other):
        return self.title == other