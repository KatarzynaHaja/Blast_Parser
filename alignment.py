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

    def print_sequence(self):
       first =  [self.qseq[i:i + 200] for i in range(0, len(self.qseq), 200)]
       second = [self.k[i:i + 200] for i in range(0, len(self.k), 200)]
       third = [self.hseq[i:i + 200] for i in range(0, len(self.hseq), 200)]
       print(len(first))
       print(len(second))
       print(len(third))
       # for i in range(min(len(first),len(third))):
       #     print()
       #     print(first[i])
       #     print(second[i])
       #     print(third[i])