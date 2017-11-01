import sqlite3
from math import ceil


class DataManager:
    def __init__(self, database_path, mfa_seq_folder_path):  # TODO: Include MFA-Seq data in database
        self.database_path = database_path
        self.mfa_seq_folder_path = mfa_seq_folder_path

    def select_chromosomes_from_database(self, **kwargs):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        for key, value in kwargs.items():
            query = 'SELECT * FROM Chromosome WHERE ' + key + ' = ?'
            cursor.execute(query, (value,))

        chromosome_tuples = cursor.fetchall()
        db.close()
        return chromosome_tuples

    def probability_landscape(self, code, length):
        scores = []
        with open(self.mfa_seq_folder_path + code + '.txt') as mfa_seq_file:
            for line in mfa_seq_file:
                scores.append(float(line))

        probability_landscape = [0] * length
        step = int(ceil(length/len(scores)))
        max_score = max(scores)

        for i, score in enumerate(scores):
            for j in range(i * step, (i + 1) * step):
                probability_landscape[j] = (score/max_score)
                if j == length - 1:
                    return probability_landscape

    def chromosomes(self, organism):
        chromosomes = []
        chromosome_tuples = self.select_chromosomes_from_database(organism=organism)
        for t in chromosome_tuples:
            chromosomes.append({'code': t[0],
                                'length': t[1],
                                'probability_landscape': self.probability_landscape(code=t[0], length=t[1])})

        return chromosomes