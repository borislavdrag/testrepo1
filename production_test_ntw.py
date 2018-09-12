import re
import math

def slovom(base):

    digits = {0:"", 1:"един", 2:"два", 3:"три", 4:"четири", 5:"пет", 6:"шест", 7:"седем", 8:"осем", 9:"девет"}
    special_names = [[" хиляда", " хиляди"], [" милион", " милиона"], [" милиард", " милиарда"]]
    currencies = [[" лев", " лева"], [" евро", " евро"]]
    currencies2 = [[" стотинка", " стотинки"], [" цент", " цента"]]

    # handles one and two digit inputs
    def two_digit(n):
        if  len(str(n)) is 1:
            return digits[n]

        if n is 10:
            return "десет"
        elif n is 11:
            return "единадесет"
        elif n//10 is 1:
            return digits[n%10] + "надесет"
        else:
            return digits[n//10] + "десет " + digits[n%10]

    #handles three digit inputs
    def three_digit(n):
        # redirects wrong input to the two_digit function
        if  len(str(n)) < 3:
            return two_digit(n)

        if n//100 is 1:
            return "сто " + two_digit(n%100)
        elif n//100 is 2:
            return "двеста " + two_digit(n%100)
        elif n//100 is 3:
            return "триста " + two_digit(n%100)
        else:
            return digits[n//100] + "стотин " + two_digit(n%100)

    def assemble(ns):
        # the input is divided into parts of 3 digits (with regular expressions)
        # to do that we pad the input with enough zeros so that its length is a multiple of 3 (with zfill() and a custom function)
        ns = list(map(lambda x: int(x), re.findall('.{1,3}', str(ns).zfill(3*int(math.ceil(len(str(ns))/float(3)))))))

        # converts all parts to words, adds an " и " if needed and reverses the list
        ns2 = list(map(lambda n: three_digit(n)[::-1].strip().replace(" ", " и ", 1)[::-1], ns))[::-1]

        # adds all names from special_names
        for i in range(len(ns2)-1):
            if ns2[i-len(ns)+1]:
                ns2[i-len(ns)+1] += special_names[i][0 if ns[len(ns)-i-2] is 1 else 1]
        ns2 = ns2[::-1]  # revert list to normal

        ns2 = list(filter(None, ns2))
        # if we don't have an " и " in the last part, and the last part is not an empty string and we have more than one part we add a next to last "и"
        if " и " not in ns2[-1] and ns2[-1] and len(ns2) > 1:
            ns2.insert(-1, "и")

        # joins and removes empty strings
        result = " ".join(list(filter(lambda a: a, ns2)))
        if "един хиляди" in result:
            result = result.replace("един хиляди", "една хиляди")
        elif "два хиляди" in result:
            result = result.replace("два хиляди", "две хиляди")
        elif "един хиляда" in result:
            result = result.replace("един хиляда", "хиляда")

        return result


    num_in_words = assemble(int(base))

    return num_in_words

while True:
    print(slovom(int(input())))
