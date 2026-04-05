/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_init.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/30 10:28:28 by Tsellak           #+#    #+#             */
/*   Updated: 2026/01/07 10:42:48 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "checker.h"

int	is_sorted(t_stack *stack)
{
	if (!stack)
		return (1);
	while (stack->next)
	{
		if (stack->value > stack->next->value)
			return (0);
		stack = stack->next;
	}
	return (1);
}

static void	append_node(t_stack **stack, int n)
{
	t_stack	*node;
	t_stack	*last_node;

	if (!stack)
		return ;
	node = malloc(sizeof(t_stack));
	if (!node)
		return ;
	node->next = NULL;
	node->value = n;
	if (*stack == NULL)
		*stack = node;
	else
	{
		last_node = ft_lstlast(*stack);
		last_node->next = node;
	}
}

void	stack_init(t_stack **a, char **args)
{
	long	n;
	int		i;

	i = 0;
	while (args[i])
	{
		if (!is_number(args[i]))
			error_exit(a, args);
		n = ft_atol(args[i]);
		if (n > INT_MAX || n < INT_MIN)
			error_exit(a, args);
		if (has_duplicates(*a, n))
			error_exit(a, args);
		append_node(a, n);
		i++;
	}
}
