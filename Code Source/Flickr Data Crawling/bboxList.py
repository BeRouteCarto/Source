# coding=utf-8
class getbboxList:
	def __init__(self):
		self.bbox = "11.3608, 48.0616, 11.7229, 48.2482"
		self.bottomleft_x = 48.0616
		self.bottomleft_y = 11.3608
		self.upright_x = 48.2482
		self.upright_y = 11.7229
		#divide the area into 100 boxes but we just need 81 points to get all the boxes
	def splitArea(self):
		diffy = (self.upright_y - self.bottomleft_y)/9
		diffx = (self.upright_x - self.bottomleft_x)/9
		# print diff
		x = []
		y = []
		for i in range(9):
			# print i
			x.append(i*diffy + self.bottomleft_y)
		for i in range(9):
			# print i
			y.append(i*diffx + self.bottomleft_x)
		bboxT = []
		for xx in x:
			for yy in y:
				# print xx,yy
				bboxT.append([xx,yy])
		bboxlist = []
		for i in range(len(bboxT)):
			# print type(bbox1[i])
			y1 = bboxT[i][0]
			x1 = bboxT[i][1]
			y2 = bboxT[i][0] + diffy
			x2 = bboxT[i][1] + diffx
			bboxlist.append([y1,x1,y2,x2])
			# bbox2 = bbox1[i] + [diffx, diffy]
			# print bbox2
		print("The area has been divided into 100 boxes")
		return bboxlist
# test = bboxList()
# bboxlist = test.splitArea()
# for i in bboxlist:
# 	print type(str(i))