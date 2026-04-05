SRCS = ft_printf.c \
       ft_print_char.c \
       ft_print_str.c \
       ft_print_ptr.c \
       ft_print_deci.c \
       ft_print_unsigned.c \
       ft_print_hex.c

NAME = libftprintf.a
CC = cc
CFLAGS = -Wall -Wextra -Werror
AR = ar rcs
RM = rm -f

OBJ = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJ) $(LIBFT_A)
	$(AR) $(NAME) $(OBJ)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re