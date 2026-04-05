def ft_count_harvest_recursive(i=1, day=None):
    if day is None:
        day = int(input("Days until harvest: "))
    if i > day:
        print("Harvest time!")
        return
    print("Day", i)
    ft_count_harvest_recursive(i+1, day)
