#coding: utf-8
import sys
sys.dont_write_bytecode = True
from server.Server import *

class Core:
	@staticmethod
	def main():
		Server().start()

if __name__ == "__main__":
	Core.main()