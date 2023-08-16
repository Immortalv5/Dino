from generation import Generation

def main():
    generation = Generation()
    generation_id = 0
    while True:
        generation.execute()
        print("Done")
        generation.keep_best_genomes()
        print("Storing")
        generation.save_genomes(generation_id)
        print('Serialization')
        generation.mutations()
        print("Mutated")
        generation_id += 1

if __name__ == '__main__':
    main()