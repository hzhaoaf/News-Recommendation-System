#conding=utf8

from config import data_dir, user_candidate_newsids_path
lines = open(user_candidate_newsids_path, 'r').readlines()

res = []
for l in lines:
    parts = l.split(':')
    nids = parts[2].split(',')
    for nid in nids[:10]:
        res.append((parts[0], nid))

fw = open(data_dir + 'test_candidate.txt', 'w+')
fw.write('userid,newsid\n')
fw.write('\n'.join(['%s,%s' % (uid, nid) for uid, nid in res]))
fw.close()
