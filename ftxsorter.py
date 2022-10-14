import math
import random


# sp = "18SUJ7039565695"


class Node:
	"""
	Class describing a single land nav point, and all associated data
	"""
	mgrs: str  # The MGRS coordinate
	coord: str  # The Raw numeric coordinate without preceding 100,000 meter designator
	label: str  # Point Label
	x: int  # X coord in meter
	y: int  # Y coord in meters
	visited: int  # has the point been visited
	other_nodes: dict[str, "Node"]  # Neighbor nodes

	def __init__(self, mgrs: str, label: str):
		self.mgrs = mgrs
		self.coord = mgrs.replace("18SUJ", "")
		self.label = label
		self.x = int(self.coord[0:5])
		self.y = int(self.coord[5:10])
		self.visited = 0
		self.other_nodes = {}

	def distance_calc(self, other: "Node") -> int:
		"""
		Distance between 2 MGRS points
		:param other: the other point
		:return: an int value, to the nearest meter
		"""
		return int(math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2))

	def add_node(self, other: "Node", label: str) -> None:
		"""
		add a node to neighbors
		:param other: the other node to add
		:param label: that nodes label
		"""
		self.other_nodes[label] = other

	def add_nodes(self, node_list: dict[str, "Node"], labels: str) -> None:
		"""
		Add a list of nodes
		:param node_list: list of nodes to add in dict
		:param labels: labels which are neighbors
		"""
		for label in labels:
			self.add_node(node_list[label], label)
		# Start point is always a neighbor
		self.other_nodes["SP1"] = Node("18SUJ7039565695", "SP1")

	def is_visited(self) -> bool:
		"""
		Check if visited yet
		:return: True if visited
		"""
		if self.visited == 0:
			return False
		return True

	def visit(self):
		self.visited = 1

	def unvisit(self):
		self.visited = 0


def main():
	"""
	Generate lanes and write them to a csv
	"""
	lanes3s = generate_lanes(create_forest(), 8, 5000, 3500)
	lanes2s = generate_lanes(create_forest(), 6, 4700, 3200)
	lanes1s = generate_lanes(create_forest(), 6, 4000, 3000)
	with open("lanes3.csv", "a") as f:
		f.write(f"Cadet, Start Point,1,2,3,4,5,6,7,8,Solution,1,2,3,4,5,6,7,8\n")
		write_csv(f, lanes3s)
	with open("lanes2.csv", "a") as f:
		f.write(f"Cadet, Start Point,1,2,3,4,5,6,Solution,1,2,3,4,5,6\n")
		write_csv(f, lanes2s)
	with open("lanes1.csv", "a") as f:
		f.write(f"Cadet, Start Point,1,2,3,4,5,6,Solution,1,2,3,4,5,6\n")
		write_csv(f, lanes1s)


def write_csv(f, lanes: list[tuple[list[str], int]]) -> None:
	"""
	Write lanes to the csv file
	:param f: the TextIO Object
	:param lanes: the list of point
	"""
	for lane in lanes:
		for point in lane[0]:
			p = point.split(' - ')
			f.write(f",{p[1]}")
		for point in lane[0]:
			p = point.split(' - ')
			f.write(f",{p[0]}")
		f.write("\n")


def generate_lanes(nodes: dict[str, Node], hops: int, max_len: int, min_len: int) -> list[tuple[list[str], int]]:
	"""
	Generate a list of lanes with the specified parameters
	:param nodes: list of previously generated nodes
	:param hops: max number of non start point nodes to visit
	:param max_len: max length of path
	:param min_len: min length of path
	:return:
	"""
	nodes["SP1"].visit()
	paths = []
	for i in range(0, 5000):
		path = travel(nodes["SP1"], 0, ["SP1"], hops)
		if path is not None and path not in paths and max_len > path[1] > min_len:
			path[0].pop(-1)
			for j in range(0, len(path[0])):
				path[0][j] += f" - {nodes[path[0][j]].mgrs}"
			paths.append(path)
	print(f"Generated {len(paths)} valid lanes of length {hops} and distance between {max_len} and {min_len}")
	return paths


def travel(node: "Node", size: int, path: list[str], hops: int) -> tuple[list[str], int]:
	"""
	Recursively travel from node to random node, not repeating the journey
	:param node: the current node being visited
	:param size: the current distance walked
	:param path: the current path taken
	:param hops: the max number of point allowed
	:return: a tuple with path and total length of path
	"""
	vals = list(node.other_nodes.values())
	random.shuffle(vals)
	for item in vals:
		if item.visited == 0:
			if item.label != node.label and item.label not in path and len(path) < hops + 1:
				path.append(item.label)
				if len(path) == hops + 1:
					# Return to SP1
					path.append("SP1")
					size += node.distance_calc(node.other_nodes["SP1"]) + node.distance_calc(item)
					return path, size
				return travel(item, size + node.distance_calc(item), path, hops)
	node.visit()


def create_forest() -> dict[str, "Node"]:
	"""
	Generates a fresh list of nodes to parse
	:return: a dict containing all nodes
	"""
	labels = """SP1
	A
	B
	C
	D
	E
	F
	G
	H
	I
	J
	K
	L
	M
	N
	O
	P
	Q
	R
	T
	U
	V
	W
	X
	Y
	Z"""
	points = """18SUJ7039565695
	18SUJ7024866158
	18SUJ7090466227
	18SUJ7105365793
	18SUJ7053765625
	18SUJ7018865635
	18SUJ7067165804
	18SUJ7084565460
	18SUJ7012965262
	18SUJ7021766352
	18SUJ7021766040
	18SUJ7014465840
	18SUJ7116166434
	18SUJ7007765566
	18SUJ7104566130
	18SUJ7076466509
	18SUJ7041666237
	18SUJ7002265328
	18SUJ7021065920
	18SUJ7035066427
	18SUJ7070865948
	18SUJ7072665649
	18SUJ7100765931
	18SUJ7092066013
	18SUJ7066766419
	18SUJ7118766214"""
	nodes = {}
	points = points.split()
	labels = labels.split()

	for i in range(0, len(labels)):
		nodes[labels[i]] = Node(points[i], labels[i])

	nodes["SP1"].add_nodes(nodes, "ABCDEFGHIJKLMNOPQRTUVWXYZ")
	nodes["A"].add_nodes(nodes, "JPIT")
	nodes["B"].add_nodes(nodes, "YONZLX")
	nodes["C"].add_nodes(nodes, "WXUFVG")
	nodes["D"].add_nodes(nodes, "VFG")
	nodes["E"].add_nodes(nodes, "DMKHQ")
	nodes["F"].add_nodes(nodes, "UVDRXWC")
	nodes["G"].add_nodes(nodes, "DVCH")
	nodes["H"].add_nodes(nodes, "QMDVG")
	nodes["I"].add_nodes(nodes, "TPAJ")
	nodes["J"].add_nodes(nodes, "KRAPA")
	nodes["K"].add_nodes(nodes, "REMJ")
	nodes["L"].add_nodes(nodes, "ZNBOY")
	nodes["M"].add_nodes(nodes, "QHEKR")
	nodes["N"].add_nodes(nodes, "LZBXWC")
	nodes["O"].add_nodes(nodes, "TYLB")
	nodes["P"].add_nodes(nodes, "JAITYUB")
	nodes["Q"].add_nodes(nodes, "HMEDK")
	nodes["R"].add_nodes(nodes, "KJAE")
	nodes["T"].add_nodes(nodes, "IPYOB")
	nodes["U"].add_nodes(nodes, "FVXWBR")
	nodes["V"].add_nodes(nodes, "DFGC")
	nodes["W"].add_nodes(nodes, "XCNUFV")
	nodes["X"].add_nodes(nodes, "BNZWCUF")
	nodes["Y"].add_nodes(nodes, "OTPLB")
	nodes["Z"].add_nodes(nodes, "LBN")

	return nodes


if __name__ == '__main__':
	main()
