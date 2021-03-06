from make_example import example, text_example, random_example

def make_data(file_name : str, dataset : str, generator : example, min_len : int, max_len : int,  num : int):
    data = open(file_name, "w")
    if dataset == "train":
        data.write("defI: 0\ndefT: 0\n")
    if dataset == "test":
        data.write("defI: 0\ndefT: nan\n")
    for i in range(num):
        data.write("\n")
        data.write(f"# {i}\n")
        sent = generator.generate_sentence(min_len, max_len)
        data.write(f"name: {sent.replace(' ', '_')}\n")
        data.write(generator.example_string(sent, dataset))
        data.write("\n")
    data.close()

if __name__ == "__main__":
    generator = random_example("example generator\common_words.txt")
    make_data("network/word-diffrand_ex.txt", "train", generator, 10, 20, 10000)
    make_data("network/word-diffrand.test_ex.txt", "test", generator, 10, 20, 1000)
    generator = text_example("example generator\Thing_Explainer.txt")
    make_data("network/word-difftext_ex.txt", "train", generator, 10, 20, 10000)
    make_data("network/word-difftext.test_ex.txt", "test", generator, 10, 20, 1000)
