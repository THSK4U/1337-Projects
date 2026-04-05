/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing_utils.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/30 10:27:34 by Tsellak           #+#    #+#             */
/*   Updated: 2025/12/30 10:51:02 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_number(char *str)
{
	int	i;

	i = 0;
	if (str[0] == '-' || str[0] == '+')
		i++;
	if (!str[i])
		return (0);
	while (str[i])
	{
		if (!ft_isdigit(str[i]))
			return (0);
		i++;
	}
	return (1);
}

int	has_duplicates(t_stack *a, int n)
{
	if (!a)
		return (0);
	while (a)
	{
		if (a->value == n)
			return (1);
		a = a->next;
	}
	return (0);
}

void	assign_index(t_stack *stack)
{
	t_stack	*node;
	t_stack	*compare;
	size_t	i;

	node = stack;
	while (node)
	{
		i = 0;
		compare = stack;
		while (compare)
		{
			if (compare->value < node->value)
				i++;
			compare = compare->next;
		}
		node->index = i;
		node = node->next;
	}
}
