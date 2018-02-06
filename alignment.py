class Alignment:
    def __init__(self, title, bit_score, correct_procent, gap, identities, align_lenth, qseq, hseq, k):
        """
        :param title: Title of alignment
        :param bit_score: Score
        :param correct_procent:percent -> identities/length
        :param gap: number of gaps
        :param identities: identities
        :param align_lenth: length of alignment
        :param qseq: seq
        :param hseq: seq
        :param k: seq
        Class contains all information about alignment
        """
        self.title = title
        self.bit_score = bit_score
        self.correct_procent = correct_procent
        self.gap = gap
        self.identities = identities
        self.align_length = align_lenth
        self.qseq = qseq
        self.hseq = hseq
        self.k = k
