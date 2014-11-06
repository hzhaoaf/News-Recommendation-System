import recsys.algorithm
from recsys.algorithm.factorize import SVD

class NewsRec():
	def __init__(self):
		self.svd = SVD()
		self.test_set = []

	def load_data(self,filename = 'train_set_for_svd'):
		self.svd.load_data(filename,sep='\t',format={'value':0,'row':2,'col':1,'ids':int})
	
	def load_test(self,filename = 'test_set_for_svd'):
		with open(filename,'r') as f:
			for line in f:
				strs = line.split('\t')
				self.test_set.append((int(strs[1]),int(strs[2])))

	def recom(self,user_id,recom_num=3,only_unknown=True):
		try:
			#index = self.svd._matrix._matrix.col_index(user_id)
			index = user_id
			return self.svd.recommend(index,recom_num,only_unknowns=only_unknown,is_row=False)
		except IndexError as e:
			return -1

	def compute(self,k = 100):
		self.svd.compute(k=k, min_values=None, pre_normalize=None, mean_center=False, post_normalize=True)

	def test(self,recom_num=3):
		hit_cnt = 0
		self.ret = []
		for user,item in self.test_set:
			re = self.recom(user,recom_num)
			#print re
			if type(re) !=	type([]):
				continue
			try:
				#item_index = self.svd._matrix._matrix.row_index(item)
				item_index = item
			except KeyError as e:
				continue
			for rec_index,rec_rate in re:
				self.ret.append((user,rec_index))
				if item_index == rec_index:
					hit_cnt += 1
		if hit_cnt == 0:
			return
		user_sum = len(self.test_set)
		recom_sum = recom_num * user_sum
		precise = float(hit_cnt) / recom_sum
		recall = float(hit_cnt) / user_sum
		f = 2.0 / (( 1.0 / precise) + (1.0 / recall))
		print 'hit:',hit_cnt
		print 'precise:',precise
		print 'recall:',recall
		print 'F:',f

	def print_ret(self,filename):
		string = ["userid,newsid\n"]
		for user,item in self.ret:
			string.append(str(user))
			string.append(',')
			string.append(str(item))
			string.append('\n')
		with open(filename,'w') as f:
			f.write("".join(string))
		

if __name__ == '__main__':
	recsys.algorithm.VERBOSE = True
	rec = NewsRec()
	rec.load_data('all_set_for_svd')
	rec.load_test('test_set_for_svd')
	rec.compute(15)
	rec.test(2)
	rec.print_ret('svd_recom2.CSV')
