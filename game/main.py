from shapes import ALL_SHAPES


def print_shapes(list_of_shapes: list = ALL_SHAPES):
    for list_of_rotations in list_of_shapes:
        print('\n\n Shape:', end='')
        for rotated_shape in list_of_rotations:
            print()
            for row_list in rotated_shape:
                print()
                for elem in row_list:
                    if elem:
                        print('*', end='')
                    else:
                        print(' ', end='')


def main():
    print_shapes()


if __name__ == "__main__":
    main()
