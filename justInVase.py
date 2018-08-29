        ans = {}
        ans['nodes'] = temp['nodes']
        ans['links'] = []
        for link in temp['links']:
            a = {'from':link['source'], 'to':link['target']}
            ans['links'].append(a)
