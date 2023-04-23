if __name__ == '__main__':
    txt = "apple:banana:cherry:orange"

    # setting the maxsplit parameter to 1, will return a list with 2 elements!
    x = txt.split(":", 1)[1]

    print(x)
