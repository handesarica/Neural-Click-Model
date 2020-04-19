import pprint

class TianGong_HumanLabel_Parser:
    """
     A parser for the human_label.txt provided by TianGong-ST

     Return:
      - true_relevances: a dict that true_relevances[qid][uid] = relevance_score
      - relevance_queries: information per query in human_label.txt
    """

    @staticmethod
    def parse(label_filename):
        label_reader = open(label_filename, "r")
        relevance_queries = []
        query_count = dict()
        true_relevances = dict()

        for line in label_reader:
            entry_array = line.strip().split('\t')
            id = int(entry_array[0])
            task = entry_array[1]
            query = entry_array[2]
            result = entry_array[3]
            relevance = int(entry_array[4])
            
            # generate true_relevance
            if not query in true_relevances:
                true_relevances[query] = dict()
                query_count[query] = 0
            if not result in true_relevances[query]:
                true_relevances[query][result] = relevance
                query_count[query] += 1
            elif true_relevances[query][result] != relevance:
                # if find a disagreement for the same query and result, compute the average value
                true_relevances[query][result] = (1.0 * true_relevances[query][result] * query_count[query] + relevance) / (query_count[query] + 1)

            # The first line of a query
            if id > len(relevance_queries):
                info_per_query = dict()
                info_per_query['sid'] = task
                info_per_query['qid'] = query
                info_per_query['uids'] = [result]
                relevance_queries.append(info_per_query)
            
            # The rest lines of a query
            else:
                relevance_queries[-1]['uids'].append(result)

        return relevance_queries, true_relevances
