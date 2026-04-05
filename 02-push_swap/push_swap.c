/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/30 10:30:08 by Tsellak           #+#    #+#             */
/*   Updated: 2026/01/07 00:08:40 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	select_sort(t_stack **a, t_stack **b)
{
	int	size;

	if (is_sorted(*a))
		return ;
	size = ft_lstsize(*a);
	if (size <= 1)
		return ;
	else if (size == 2)
	{
		if ((*a)->value > (*a)->next->value)
			sa(a);
	}
	else if (size == 3)
		sort_3(a);
	else if (size <= 5)
	{
		assign_index(*a);
		sort_small(a, b, size);
	}
	else
	{
		assign_index(*a);
		chunk(a, b);
		push_back(a, b, size - 1);
	}
}

static void	push_swap(t_stack **a, char **argv)
{
	char	**args;
	int		i;

	i = 0;
	while (argv[i])
	{
		args = ft_split(argv[i], ' ');
		if (!args || !args[0])
			error_exit(a, args);
		stack_init(a, args);
		free_matrix(args);
		i++;
	}
}

int	main(int argc, char **argv)
{
	t_stack	*a;
	t_stack	*b;

	a = NULL;
	b = NULL;
	if (argc < 2 || (argc == 2 && !argv[1][0]))
		return (0);
	push_swap(&a, argv + 1);
	select_sort(&a, &b);
	free_stack(&a);
	return (0);
}
