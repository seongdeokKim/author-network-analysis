import operator
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


class CitedPaper:

    def __init__(self, citing_paper_eid: str,
                 cited_paper_title: 'str',
                 cited_paper_authors: 'list of str'):

        self._citing_paper_eid = citing_paper_eid
        self._cited_paper_title = cited_paper_title
        self._cited_authors = cited_paper_authors

    @property
    def citing_paper_eid(self):
        return self._citing_paper_eid

    @citing_paper_eid.setter
    def citing_paper_eid(self, value: str):
        if not value.startswith("2-s2.0-"):
            raise ValueError("wrong eid allocated")
        else:
            self._citing_paper_eid = value

    @property
    def cited_paper_title(self):
        return self._cited_paper_title

    @property
    def cited_paper_authors(self):
        return self._cited_authors


if __name__ == '__main__':

    input_file = './data/dataset_for_author_co-citation.txt'
    output_file = 'author_co-citation_network.txt'

    # set cited paper's info., such as paper and authors, to citing paper object
    citing_paper_dict = {}
    with open(input_file, 'r', encoding='utf-8') as fr:
        for i, line in enumerate(fr):
            if i != 0:
                field_line = line.strip().split('\t')

                try: citing_paper_eid=field_line[1].strip()
                except IndexError: continue

                try: cited_paper_title = field_line[4].strip()
                except IndexError: continue

                try: cited_paper_authors = field_line[5].strip()
                except IndexError: continue

                if citing_paper_eid != '' and cited_paper_authors != '':
                    cited_paper_authors = [author.strip() for author in cited_paper_authors.split(';')]
                    cited_paper_authors = list(set(cited_paper_authors))

                    cited_paper = CitedPaper(citing_paper_eid=citing_paper_eid,
                                             cited_paper_title=cited_paper_title,
                                             cited_paper_authors=cited_paper_authors)

                    if citing_paper_eid not in citing_paper_dict.keys():
                        citing_paper_dict[citing_paper_eid] = [cited_paper]
                    else:
                        citing_paper_dict[citing_paper_eid].append(cited_paper)

    # compute co_occurence between authors that belong to different paper, but are cited by same paper
    author_dict = AuthorDict()
    co_occur_counter = {}
    for citing_paper_eid, cited_papers in citing_paper_dict.items():
        if len(cited_papers) > 1:

            for i in range(len(cited_papers)):
                i_author_ids = [author_dict.get_id_or_add(author) for author in cited_papers[i].cited_paper_authors]
                for j in range(i+1, len(cited_papers)):
                    j_author_ids = [author_dict.get_id_or_add(author) for author in cited_papers[j].cited_paper_authors]

                    for i_author_id in i_author_ids:
                        for j_author_id in j_author_ids:

                            if i_author_id > j_author_id:
                                pair = (j_author_id, i_author_id)
                            else:
                                pair = (i_author_id, j_author_id)

                            if pair not in co_occur_counter.keys():
                                co_occur_counter[pair] = 1
                            else:
                                co_occur_counter[pair] += 1

    # sort and store
    with open(output_file, 'w', encoding='utf-8') as fw:
        sorted_dict = sorted(co_occur_counter.items(), key=operator.itemgetter(-1), reverse=True)
        for (a1_id, a2_id), freq in sorted_dict:
            print(f'{author_dict.get_author(a1_id)}\t{author_dict.get_author(a2_id)}\t{freq}')
            fw.write(f'{author_dict.get_author(a1_id)}\t{author_dict.get_author(a2_id)}\t{freq}\n')


    # convert co-occurence file to graphml file for further visualization through gephi software
    convert_co_occur_to_graphml(output_file, threshold=2)