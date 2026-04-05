CC= cc
CFLAGS= -Wall -Werror -Wextra
SRC=	push.c \
		reverse_r.c \
		rotate.c \
		swap.c \
		ft_atol.c \
		ft_isdigit.c \
		ft_lstlast.c \
		ft_lstsize.c \
		ft_new_node.c \
		ft_split.c \
		ft_strlen.c \
		ft_substr.c \
		big_sort.c \
		free_utils.c \
		parsing_utils.c \
		push_swap.c \
		small_sort.c \
		stack_init.c

BONUS=	bonus/checker.c \
		bonus/free_utils.c \
		bonus/ft_atol.c \
		bonus/ft_isdigit.c \
		bonus/ft_lstlast.c \
		bonus/ft_split.c \
		bonus/ft_strlen.c \
		bonus/ft_substr.c \
		bonus/parsing_utils.c \
		bonus/push.c \
		bonus/reverse_r.c \
		bonus/rotate.c \
		bonus/stack_init.c \
		bonus/swap.c \
		bonus/get_next_line_utils.c \
		bonus/get_next_line.c

NAME= push_swap
NAME_BONUS= checker
RM = rm -f

OBJ= $(SRC:.c=.o)
OBJ_BONUS= $(BONUS:.c=.o)

all: $(NAME)

bonus: $(NAME_BONUS)

$(NAME): $(OBJ)
	$(CC)  $(CFLAGS) $^ -o $@

$(NAME_BONUS): $(OBJ_BONUS)
	$(CC)  $(CFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJ) $(OBJ_BONUS)

fclean: clean
	$(RM) $(NAME) $(NAME_BONUS)

re: fclean $(NAME) $(NAME_BONUS)

.PHONY: all clean fclean re
