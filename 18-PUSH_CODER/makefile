NAME = codexion
CC = gcc
CFLAGS = -Wall -Wextra -Werror -pthread
SRC_DIR = coders
SRCS = main.c logger.c init.c coder.c dongle.c scheduler.c heap.c monitor.c time_utils.c cleanup.c
OBJS = $(addprefix $(SRC_DIR)/, $(SRCS:.c=.o))

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

$(SRC_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all
