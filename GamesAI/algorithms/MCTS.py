#Inspired by following MCTS implementation : https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
import random
from collections import defaultdict
import math
from typing import Iterable

from GamesAI.div.GameContent import State, GameType, ActionType
from GamesAI.Player import Player
from GamesAI.div.utils import argmax

NodeType = object

class Node:
    """
    A representation of a single state.
    MCTS works by constructing a tree of these Nodes.
    """
    def __init__(self, state : State, game : GameType, player : Player) -> None:
        self.state = state
        self.game = game
        self.player = player

    def find_children(self) -> Iterable[object]:
        "Return all possible successors of this node"
        childrens = list()
        for action in self.game.get_actions(self.state):
            state = self.game.get_result(self.state, action)
            childrens.append(Node(state = state, game = self.game, player = self.player))
        return childrens
    
    def find_random_child(self) -> object:
        "Random successor of this board state (for more efficient simulation)"
        actions = self.game.get_actions(self.state)
        action = random.choice(actions)
        state = state = self.game.get_result(self.state, action)
        return Node(state = state, game = self.game, player = self.game.get_player_playing(state))

    def is_terminal(self) -> bool:
        "Returns True if the node has no children"
        return self.game.is_terminal_state(self.state)

    def __hash__(self) -> int:
        "Nodes must be hashable"
        return hash(self.state)

    def __eq__(node1, node2) -> bool:
        "Nodes must be comparable"
        return node1.state == node2.state
    
    

class MonteCarloTreeSearch(Player):
    """Player that uses Monte-Carlo Tree Search method for evaluating node.
    Only works for 2 player games, deterministic, zero-sum game."""
    agent_name = "MCTS"
    
    def __init__(self, game: GameType, game_name: str, agent_name: str, n_rollouts : int = 50) -> None:
        super().__init__(game, game_name, agent_name)
        self.n_rollouts = n_rollouts
        if len(game.names) != 2:
            raise ValueError("MCTS can only be used for 2 player games")
        self.Q = defaultdict(int)  # total utility of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = 1.4  # exploration weight, should scale with the typical variational utility. Utility variation of 1 <=> exploration_weight of 1.4.
        

    def get_action(self, state: State) -> ActionType:

        "Choose the best successor of node. (Choose a move in the game)"
        node = Node(state = state, game = self.game, player = self) 
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")
        
        for _ in range(self.n_rollouts):
            self.do_rollout(node)
        
        if node not in self.children:
            return node.find_random_child()
        
        def score(action : ActionType):
            n = Node(state = self.game.get_result(state, action), game = self.game, player = self)
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average utility

        return argmax(indexes = self.game.get_actions(state), func = score)

    def do_rollout(self, node : Node) -> None:
        "Make the tree one layer better. (Train for one iteration.)"
        path = self.select(node)
        leaf = path[-1]
        self.expand(leaf)
        utilities = self.simulate(leaf)
        self.backpropagate(path, utilities)

    def select(self, node):
        "Find an unexplored descendent of a node, return the path leading from node to this descendent."
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self.uct_select(node)  # descend a layer deeper

    def expand(self, node : Node) -> None:
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def simulate(self, node : Node) -> dict[Player, float]:
        "Returns the utilities for a random simulation of a node"
        while True:
            if node.is_terminal():
                return self.game.get_utilities(node.state)
            node = node.find_random_child()

    def backpropagate(self, path : list[Node], utilities : dict[Player, float]) -> None:
        "Send the utilities back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += utilities[node.player]

    def uct_select(self, node : Node) -> Node:
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)