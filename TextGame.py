from tkinter import *
class Graph:
	def __init__(self, graph_dict = None, vertexset = None, edgeset = None):
		if graph_dict != None:
			self.graph_dict = graph_dict
		
		if graph_dict == None and vertexset != None and edgeset != None:
			self.graph_dict = self.constructGraphDictionary(vertexset,edgeset)
		
		if graph_dict == None and vertexset == None and edgeset == None:
			self.graph_dict = {}
	
	def addVertex(self, v):
		if v not in self.graph_dict:
			self.graph_dict[v] = []
	
	def addEdge(self,e):
		if e[0] not in self.graph_dict:
			return
		self.graph_dict[e[0]].append(e[1])
	
	def getVertices(self):
		return set(self.graph_dict.keys())
	
	def getEdges(self):
		return self.__generateEdges(self.graph_dict)
	
	def __generateEdges(self, edgeset):
		list = []
		for i in edgeset:
			for j in edgeset[i]:
				list.append((i,j))
		return set(list)
	
	def constructGraphDictionary(self, vertexset, edgeset):
		graph_dict = {}
		
		for i in vertexset:
			graph_dict[i] = []
		
		for i in edgeset:
			if i[0] in graph_dict and i[1] in graph_dict:
				graph_dict[i[0]].append(i[1])
		
		return graph_dict
				
		
class GameStates(Graph):
	def __init__(self):
		super().__init__()
		self.graph_dict = {'bed':['door','window'],
						   'door':['bed','window', 'hallway'],
						   'window':['bed','door'],
						   'hallway':['bathroom','living room','door'],
						   'bathroom':['hallway'],
						   'living room':['hallway']}
		self.vertex_properties = {"bed":"You are on the bed.There is a door and a window",
								  "door":"You are at the door.It's meowing on the other side",
								  "window":"you see a kitten looking at you from outside, you feel happy",
								  "hallway":"you are in the hallway u here cute mews",
								  "bathroom":"you look pretty tired.now get that kitteh!",
								  "living room":"you are in the living room, you'll be procrastinating all day"}
		self.root = 'bed'
	
	def getRoot(self):
		return self.root
	
	def getProperties(self,v):
		return (self.vertex_properties[v], self.graph_dict[v])
	
class Walker:
	def __init__(self, gamestates):
		self.gamestates = gamestates
		self.currentVertex = self.gamestates.getRoot()
	
	def getStateProperties(self):
		return self.gamestates.getProperties(self.currentVertex)
	
	def walk(self, v):
		self.currentVertex = v
	
class GameModel:
	def __init__(self):
		self.walker = Walker(GameStates())
	
	def getGameState(self):
		return self.walker.getStateProperties()
	
	def setGameState(self, v):
		self.walker.walk(v)
		
class GameView:  #gameview needed the edit
	def __init__(self,parent):
		self.vertexPositions = {}
		self.canvas = Canvas(parent,width = 1440, height = 700, bg = "black")
		self.canvas.pack()
		self.canvaschoices = {}
		
		
	def setup(self, gamestate):
		self.canvas.create_text(700, 40,fill = "white", font="Times 20 bold", text = gamestate[0], tags = "text")
		num = 1
		choices = {}
		for i in gamestate[1]:
			self.canvas.create_text(700, num * 80, fill = "white", \
								    font="Times 20 italic bold", text = "go to " + i, \
					   	   			tags = i)
			choices[(num * 80)] = i
			num = num + 1
		self.canvaschoices = choices
			
	
	def destroyCanvasElements(self):
		self.canvas.delete("all")
	
	def getCanvas(self):
		return self.canvas
	
	def getChoice(self, choice):
		return self.canvaschoices[(choice// 80) * 80]
	
	
		

class GameController:
	def __init__(self, view, model):
		view.getCanvas().bind("<Button-1>", self.selectChoice) #bind a click event
		self.view = view
		self.model = model
		self.startup()
	
	def startup(self):
		#get files and upload to model
		self.view.setup(self.model.getGameState())
	
	def selectChoice(self, event):
		choice = self.view.getChoice(event.y)
		if choice == None:
			return
		self.view.destroyCanvasElements()
		self.model.setGameState(choice)
		self.view.setup(self.model.getGameState())
		
		
class GUI:
	def __init__(self):
		window = Tk()
		GameController(GameView(window),GameModel())
		window.mainloop()

GUI()