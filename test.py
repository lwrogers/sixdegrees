from graph_toolz import Graph
import unittest
import itertools

class GraphUnittest(unittest.TestCase):
    def setUp(self):
        """ instantiate the graph """
        self.network = Graph()
        f_input = open("dummyinput.txt", 'r', encoding="utf-8")

        all_cast = list()
        acted_in = dict()
        total = 0

        for line in f_input.readlines():
            total = total + 1
            tokens = line.split('#')
            person = tokens[0].strip()

            for i in range(1,len(tokens)):
                movie = tokens[i].strip()
                all_cast.append((movie, person))

        f_input.close()

        all_cast.sort(key = lambda tup: tup[0])

        cast = list()
        prev = ' '

        for i in range(0, len(all_cast)):
            movie = (all_cast[i])[0]
            person = (all_cast[i])[1]

            if movie == prev and i != len(all_cast)-1:
                cast.append(person)
                continue

            elif movie == prev and i==len(all_cast)-1:
                cast.append(person)

            for actor in cast:
                if actor not in acted_in:
                    acted_in[actor] = set([prev])
                else:
                    acted_in[actor].add(prev)

            for (person1, person2) in itertools.combinations(cast,2):
                    self.network.addEdge(person1, person2)

            prev = movie
            cast = [person]

    def test_path(self):
        """ test the length of the shortest path """
        self.assertEqual(len(self.network.path("A", "B")), 2)
        self.assertEqual(len(self.network.path("A", "C")), 2)
        self.assertEqual(len(self.network.path("A", "G")), 3)
        self.assertEqual(len(self.network.path("H", "G")), 4)
        self.assertEqual(len(self.network.path("B", "G")), 2)
        self.assertEqual(len(self.network.path("E", "B")), 3)

    def test_levels(self):
        """ test the levels for four different nodes """
        self.assertListEqual(self.network.levels("A"), [1, 2, 3, 2, 2, 0, 0])
        self.assertListEqual(self.network.levels("C"), [1, 2, 2, 2, 2, 1, 0])
        self.assertListEqual(self.network.levels("G"), [1, 3, 4, 2, 0, 0, 0])
        self.assertListEqual(self.network.levels("F"), [1, 2, 2, 3, 2, 0, 0])


if __name__ == '__main__':
    unittest.main()