import math


class Chromosome:
    def __init__(self, code, length, probability_landscape):
        self.code = code
        self.length = length
        self.strand = [0] * self.length
        self.activation_probabilities = probability_landscape
        self.number_of_replicated_bases = 0
        self.number_of_origins = 0

    def __len__(self):
        return self.length

    def __str__(self):
        chromosome_string = ""
        for i in range(0, len(self.strand), 500):
            chromosome_string += "{}\n".format(str(self.strand[i]))

        return chromosome_string

    def base_is_replicated(self, base):
        return True if self.strand[base] else False

    def activation_probability(self, base):
        return self.activation_probabilities[base]

    def replicate(self, start, end, time):
        if start == end:
            self.number_of_origins += 1

        is_normal_transcription = True
        if end < 0:
            is_normal_transcription = False
            end = 0

        elif end > len(self) - 1:
            is_normal_transcription = False
            end = len(self) - 1

        for i in range(start, end + int(math.copysign(1, end - start)), int(math.copysign(1, end - start))):
            if not self.strand[i]:
                self.strand[i] = time
                self.number_of_replicated_bases += 1

            elif i != start:    # The start position is always duplicated
                is_normal_transcription = False
                break

        return is_normal_transcription

    def is_replicated(self):
        return self.number_of_replicated_bases == len(self)
