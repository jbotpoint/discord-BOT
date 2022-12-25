def parse_tier_file(file):
    new_dict = {}
    with open(file) as f:
        for line in f:
            listline = line.split("|", 1)
            movie_name = listline[0]
            movie_tier = listline[1]
            movie_tier = movie_tier.replace("\n", "")
            try:
                new_dict[movie_tier].append(movie_name)
            except KeyError:
                new_dict[movie_tier] = [movie_name]
                
    return new_dict
