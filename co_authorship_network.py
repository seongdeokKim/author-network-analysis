from utils.co_occur2graphml import convert_co_occur_to_graphml

class AuthorDict:
    def __init__(self):
        self.d = {}  # author -> author_id
        self.a = []  # author_id -> author

    def get_id_or_add(self, author):
        # return author's id corresponding to that author if the author is in author_dict
        if author in self.d:
            return self.d[author]
        # otherwise, put the author in author_dict and then return newly generated author_id
        else:
            self.d[author] = len(self.d)
            self.a.append(author)
            return self.d[author]

    def get_author(self, id):
        return self.a[id]


class Paper:
    auto_generated_id = 0

    def __init__(self, eid: str, authors: 'list of str'):
        if eid.strip() == '':
            self._eid = str(Paper.auto_generated_id)
            Paper.auto_generated_id += 1
        else:
            self._eid = eid
        self._authors = authors

    @property
    def eid(self):
        return self._eid

    @property
    def authors(self):
        return self._authors


if __name__ == '__main__':

    input_file = './data/dataset_for_co-authorship.txt'
    output_file = 'co-authorship_network.txt'

    # set paper's info., such as eid and authors, to paper object
    papers = []
    with open(input_file, 'r', encoding='utf-8') as fr:
        for line in fr:
            field_line = line.strip().split('\t')

            # print(field_line)
            try: eid = field_line[1].strip()
            except IndexError: continue

            try: authors = field_line[2].strip()
            except IndexError: continue

            if eid != '' and authors != '':
                authors = [author.strip() for author in authors.split(';')]
                authors = list(set(authors))

                papers.append(
                    Paper(eid=eid,
                          authors=authors)
                )

    # compute co_occurence between authors that belong to the same paper
    co_occur_counter = {}
    author_dict = AuthorDict()
    for paper in papers:
        author_ids = [author_dict.get_id_or_add(author) for author in paper.authors]

        for i in range(len(author_ids)):
            for j in range(i+1, len(author_ids)):
                i_author_id, j_author_id = author_ids[i], author_ids[j]

                if i_author_id > j_author_id:
                    pair = (j_author_id, i_author_id)
                else:
                    pair = (i_author_id, j_author_id)

                if pair not in co_occur_counter:
                    co_occur_counter[pair] = 1
                else:
                    co_occur_counter[pair] += 1

    # sort and store
    with open(output_file, 'w', encoding='utf-8') as fw:
        sorted_dict = sorted(co_occur_counter.items(), key=lambda x: x[-1], reverse=True)
        for (a1_id, a2_id), freq in sorted_dict:
            print(f'{author_dict.get_author(a1_id)}\t{author_dict.get_author(a2_id)}\t{freq}')
            fw.write(f'{author_dict.get_author(a1_id)}\t{author_dict.get_author(a2_id)}\t{freq}\n')


    # convert co-occurence file to graphml file for further visualization through gephi software
    convert_co_occur_to_graphml(output_file, threshold=2)