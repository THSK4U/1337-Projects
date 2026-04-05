/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   big_sort.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/30 10:27:37 by Tsellak           #+#    #+#             */
/*   Updated: 2025/12/30 10:29:21 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_range(t_stack *a)
{
	int	size;

	size = ft_lstsize(a);
	if (size <= 100 && size >= 10)
		return (15);
	else if (size <= 500)
		return (30);
	else
		return ((size * 0.045) + 10);
}

static int	get_big_position(t_stack *b, int size)
{
	int	i;

	i = 0;
	while (b->index != size)
	{
		i++;
		b = b->next;
	}
	return (i);
}

void	push_back(t_stack **a, t_stack **b, int size)
{
	int	big_position;

	while (*b)
	{
		big_position = get_big_position((*b), size);
		if (big_position < size / 2)
		{
			while ((*b)->index != size)
				rb(b);
		}
		else
			while ((*b)->index != size)
				rrb(b);
		pa(a, b);
		size--;
	}
}

int	chunk(t_stack **a, t_stack **b)
{
	int	count;
	int	range;

	count = 0;
	range = get_range(*a);
	while (*a)
	{
		if ((*a)->index <= count)
		{
			pb(b, a);
			rb(b);
			count++;
		}
		else if ((*a)->index <= count + range)
		{
			pb(b, a);
			count++;
		}
		else
			ra(a);
	}
	return (count);
}
