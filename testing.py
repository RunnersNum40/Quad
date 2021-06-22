from quad import Quad
from time import sleep
if __name__ == "__main__":
	q = Quad("quad.config")
	q[0].set(150, 150, 0)
	sleep(10)
