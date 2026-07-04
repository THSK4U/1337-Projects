/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:34 by Tsellak           #+#    #+#             */
/*   Updated: 2026/07/01 03:38:09 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	compare_edf(t_coder *a, t_coder *b)
{
	if (a->deadline < b->deadline)
		return (1);
	if (a->deadline > b->deadline)
		return (0);
	if (a->id < b->id)
		return (1);
	return (0);
}

void	heap_down(t_dongle *dongle)
{
	t_coder	*tmp;
	int		i;
	int		child;
	int		smallest;

	i = 0;
	while (1)
	{
		child = (i * 2) + 1;
		if (child >= dongle->tail)
			break ;
		smallest = child;
		if (child + 1 < dongle->tail
			&& compare_edf(dongle->queue[child + 1], dongle->queue[child]))
			smallest = child + 1;
		if (compare_edf(dongle->queue[i], dongle->queue[smallest]))
			break ;
		tmp = dongle->queue[i];
		dongle->queue[i] = dongle->queue[smallest];
		dongle->queue[smallest] = tmp;
		i = smallest;
	}
}

void	heap_up(t_dongle *dongle)
{
	t_coder	*tmp;
	int		i;
	int		parent;

	i = dongle->tail - 1;
	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (!compare_edf(dongle->queue[i], dongle->queue[parent]))
			break ;
		tmp = dongle->queue[i];
		dongle->queue[i] = dongle->queue[parent];
		dongle->queue[parent] = tmp;
		i = parent;
	}
}
