/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   small_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/30 10:27:45 by Tsellak           #+#    #+#             */
/*   Updated: 2025/12/30 10:27:46 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	sort_3(t_stack **a)
{
	int	first;
	int	second;
	int	thrid;

	first = (*a)->value;
	second = (*a)->next->value;
	thrid = (*a)->next->next->value;
	if (first > second && second < thrid && first < thrid)
		sa(a);
	else if (first > second && second > thrid)
	{
		sa(a);
		rra(a);
	}
	else if (first > second && second < thrid && first > thrid)
		ra(a);
	else if (first < second && second > thrid && first < thrid)
	{
		rra(a);
		sa(a);
	}
	else if (first < second && second > thrid && first > thrid)
		rra(a);
	return (1);
}

static int	get_min_position(t_stack *a, int target)
{
	int	i;

	i = 0;
	while (a->index != target)
	{
		a = a->next;
		i++;
	}
	return (i);
}

static void	get_min(t_stack **a, t_stack **b, int target)
{
	int	size;
	int	min_position;

	size = ft_lstsize((*a));
	min_position = get_min_position((*a), target);
	while ((*a)->index != target)
	{
		if (min_position <= size / 2)
			ra(a);
		else
			rra(a);
	}
	pb(b, a);
}

int	sort_small(t_stack **a, t_stack **b, int size)
{
	int	i;

	i = 0;
	while (size > 3)
	{
		get_min(a, b, i);
		i++;
		size--;
	}
	sort_3(a);
	while (i--)
		pa(a, b);
	return (1);
}
