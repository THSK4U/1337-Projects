/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/30 10:30:08 by Tsellak           #+#    #+#             */
/*   Updated: 2026/01/07 10:43:32 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"
#include "get_next_line.h"

static int	select_ops(t_stack **a, t_stack **b, char *line)
{
	if (!ft_strcmp(line, "sa\n"))
		sa(a);
	else if (!ft_strcmp(line, "sb\n"))
		sb(b);
	else if (!ft_strcmp(line, "ss\n"))
		ss(a, b);
	else if (!ft_strcmp(line, "pa\n"))
		pa(a, b);
	else if (!ft_strcmp(line, "pb\n"))
		pb(b, a);
	else if (!ft_strcmp(line, "ra\n"))
		ra(a);
	else if (!ft_strcmp(line, "rb\n"))
		rb(b);
	else if (!ft_strcmp(line, "rr\n"))
		rr(a, b);
	else if (!ft_strcmp(line, "rra\n"))
		rra(a);
	else if (!ft_strcmp(line, "rrb\n"))
		rrb(b);
	else if (!ft_strcmp(line, "rrr\n"))
		rrr(a, b);
	else
		return (1);
	return (0);
}

static void	check_sort(t_stack **a, t_stack **b)
{
	char	*line;

	line = get_next_line(0);
	while (line)
	{
		if (select_ops(a, b, line))
		{
			free(line);
			error_exit(a, NULL);
		}
		free(line);
		line = get_next_line(0);
	}
	if (is_sorted((*a)) && (*b) == NULL)
		write(1, "OK\n", 3);
	else
		write(1, "KO\n", 3);
}

int	main(int argc, char **argv)
{
	t_stack	*a;
	t_stack	*b;
	char	**args;
	int		i;

	a = NULL;
	b = NULL;
	i = 1;
	if (argc < 2 || (argc == 2 && !argv[1][0]))
		return (0);
	while (argv[i])
	{
		args = ft_split(argv[i], ' ');
		if (!args || !args[0])
			error_exit(&a, args);
		stack_init(&a, args);
		free_matrix(args);
		i++;
	}
	check_sort(&a, &b);
	free_stack(&a);
	free_stack(&b);
	return (0);
}
