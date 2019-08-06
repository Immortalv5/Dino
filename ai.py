from generation import Generation

def main():
    generation = Generation()
    while True:
        generation.execute()
        print("Done")
        generation.keep_best_genomes()
        print("Storing")
        generation.mutations()
        print("Mutated")

if __name__ == '__main__':
    main()